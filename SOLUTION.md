# AI Interview Tutor — Solution Report

This document describes the backend for an AI-assisted technical interview platform: responsibilities of each service, shared libraries, data flows, persistence, and operational tooling. The stack is designed for **production deployment**—configuration via environment and secrets, durable asynchronous messaging, layered services, and reproducible local stacks aligned with production boundaries. For step-by-step setup commands, see [README.md](README.md).

---

## Solution summary

The repository delivers four runnable components plus a shared JWT package:

| Component | Delivery shape | Role |
|-----------|----------------|------|
| User Management | FastAPI (HTTP) | Registration, OAuth2-style token issuance, refresh-token rotation with Redis-backed reuse detection; password-reset flow integrated with notifications; Postgres for users; publishes CV-analysis and related jobs to RabbitMQ where product flows require it |
| Interview | FastAPI (HTTP + WebSocket) | LangGraph-driven conversational interview agent; bundled static HTML demo client; checkpointing configurable for single-node or scaled deployments |
| Analyze | Async worker | Consumes CV-analysis jobs from **`cv-analyze-stream`**; loads PDFs from S3; extracts text; structured LLM output to MongoDB; publishes results to **`cv-analysis-results`** for downstream consumers |
| Notification | Sync worker | Consumes password-reset jobs from RabbitMQ; persists outbound mail metadata in MongoDB; sends email via AWS SES |
| `jwt_handler` | Python library under `libs/jwt_handler` | RS256 encode/decode, token generators, DTOs — consumed by User Management |

Synchronous traffic hits User Management and Interview directly. Analyze and Notification run as workers attached to durable RabbitMQ queues and integrate with object storage, document stores, and cloud email.

---

## Architecture

The diagram below complements the static overview image in this repository.

![Architecture overview](docs/architecture-overview.png)

---

## Repository layout

| Path | Purpose |
|------|---------|
| [user-management-service/](user-management-service/) | FastAPI app, layered architecture, Alembic migrations, Redis, aio-pika producer for async integration with Analyze and Notification |
| [interview-service/](interview-service/) | REST + WebSocket API, LangGraph workflow, LLM factory, static demo under `src/static/` |
| [analyze-service/](analyze-service/) | `dependency-injector` composition root, aio-pika consumer/producer, S3/Mongo/adapters, CV analysis agent |
| [notification-service/](notification-service/) | Blocking pika consumer, reset-password use case, Mongo repository, SES adapter |
| [libs/jwt_handler/](libs/jwt_handler/) | Reusable JWT handling (`jwt_handler` package) |
| [pyproject.toml](pyproject.toml) / [poetry.lock](poetry.lock) | Root Poetry project: shared dev tooling versions |
| [.pre-commit-config.yaml](.pre-commit-config.yaml) | Formatting and lint hooks; scoped mypy |
| [.gitignore](.gitignore) | Ignores `.env`, virtualenvs, IDE dirs, bytecode |

---

## Shared library: `jwt_handler`

**Location:** [libs/jwt_handler/](libs/jwt_handler/) — package metadata in [libs/jwt_handler/pyproject.toml](libs/jwt_handler/pyproject.toml) (Python `>=3.9`; services run 3.12).

**Responsibility.** Centralize RS256 JWT creation and verification using PEM keys. Defaults for algorithm and TTL-related settings live in `jwt_handler.config` (`JWTSettings`). Configuration is **environment-first**, with optional YAML for local and development profiles.

**Core pieces.**

- [`JWTTokenHandler`](libs/jwt_handler/jwt_handler/handlers/token_handler.py) — `encode_jwt` / `decode_jwt`; maps PyJWT exceptions to library-specific errors.
- Generators and value objects under [`jwt_handler/generators/`](libs/jwt_handler/jwt_handler/generators/) and [`jwt_handler/value_objects/`](libs/jwt_handler/jwt_handler/value_objects/).
- DTOs such as `TokenInfoDTO` under [`jwt_handler/dtos`](libs/jwt_handler/jwt_handler/dtos) (imported by User Management auth flows).

**Consumption.** User Management declares `jwt-handler` as a Git dependency pointing at this monorepo’s `libs/jwt_handler` ([user-management-service/pyproject.toml](user-management-service/pyproject.toml)). For offline or forked workflows, switch to a `path` dependency.

**Imports.** The package root [`__init__.py`](libs/jwt_handler/jwt_handler/__init__.py) does not re-export the full API; prefer explicit submodule imports (`jwt_handler.models`, `jwt_handler.interfaces`, etc.), consistent with service code.

---

## User Management Service

**Entrypoint.** [user-management-service/src/main.py](user-management-service/src/main.py) — FastAPI app with routers and global exception wiring; lifespan in [user-management-service/src/lifespan.py](user-management-service/src/lifespan.py) acquires Redis and an async SQLAlchemy engine, **waits for RabbitMQ readiness** so async flows start in a defined order, then serves traffic; shutdown closes Redis and the engine.

**Configuration.** [user-management-service/src/config.py](user-management-service/src/config.py) via `pydantic-settings`: Postgres (`POSTGRES_*`), Redis, RSA keys (`PUBLIC_KEY`, `PRIVATE_KEY`), RabbitMQ URL builder and queue naming (`cv-analyze-stream` for inbound analyzer jobs aligns with Analyze), SQLAlchemy pool options.

**Layering.**

- **Domain:** entities (e.g. user, roles), repository interfaces, ports for Redis and messaging.
- **Application:** use cases for registration, login, refresh, profile CRUD, password reset, and flows that enqueue work for Analyze and Notification. Refresh flow decodes JWT, enforces `TokenType.REFRESH`, loads the user, rejects blocked accounts, and **rejects refresh reuse**: if `refresh-key:{token}` already exists in Redis, the token is treated as invalid; otherwise new access and refresh tokens are issued and the previous refresh token key is stored with a TTL matching remaining lifetime ([user-management-service/src/application/use_cases/auth/refresh_token_use_case.py](user-management-service/src/application/use_cases/auth/refresh_token_use_case.py)).
- **API:** versioned routers under [user-management-service/src/api/v1/](user-management-service/src/api/v1/); OAuth2 password flow style `tokenUrl` in [user-management-service/src/api/security.py](user-management-service/src/api/security.py).

**Auth HTTP surface** ([user-management-service/src/api/v1/endpoints/auth.py](user-management-service/src/api/v1/endpoints/auth.py)) includes:

- `POST /api/v1/auth/signup`
- `POST /api/v1/auth/token` (form username/password)
- `POST /api/v1/auth/refresh` (form refresh_token)
- `POST /api/v1/auth/reset-password` — initiate reset; delivers messages consumed by Notification ([notification-service](notification-service/))
- `POST /api/v1/auth/reset-password/{token}` — confirm reset with token

Integration coverage for this surface lives under [user-management-service/tests/integration_tests/auth/test_reset_password.py](user-management-service/tests/integration_tests/auth/test_reset_password.py).

**Messaging.** [user-management-service/src/infrastructure/rabbitmq/rabbitmq_producer.py](user-management-service/src/infrastructure/rabbitmq/rabbitmq_producer.py) implements a durable-queue, persistent-message publisher via aio-pika, used from registration, profile, and CV-submission paths to enqueue **`cv-analyze-stream`** jobs and **`reset-password-stream`** notifications as defined by the application use cases.

**Persistence.** Alembic migrations under [user-management-service/src/migrations/](user-management-service/src/migrations/); initial `users` table with uniqueness constraints on email, username, and phone.

---

## Interview Service

**Entrypoint.** [interview-service/src/main.py](interview-service/src/main.py) — mounts `/api/v1` and static files at `/static`; root `GET /` returns JSON pointing to `interview_client.html`.

**Configuration.** [interview-service/src/config.py](interview-service/src/config.py): YAML-backed logging where configured; nested LLM settings (default stack uses Google Gemini via env such as `GOOGLE_API_KEY`; optional OpenAI-compatible “custom” endpoint for local experimentation — see [interview-service/.env.example](interview-service/.env.example)).

**Agent.**

- LLM construction in [interview-service/src/agent/llm.py](interview-service/src/agent/llm.py); the graph uses module-level `llm` from `create_google_llm()` unless configured otherwise.
- Workflow in [interview-service/src/agent/workflow.py](interview-service/src/agent/workflow.py): `StateGraph` over [`InterviewState`](interview-service/src/domain/models/interview_state.py). Nodes cover greeting, soft/hard questions, small talk, wrap-up, routing, and answer evaluation. Conditional routing includes an async LLM classification step (`SMALLTALK` vs continuing questioning) driven by [interview-service/src/agent/prompts/question_router_decision.py](interview-service/src/agent/prompts/question_router_decision.py).
- **Checkpointing** uses LangGraph-compatible persistence; deployments choose an appropriate backend (for example in-process defaults for local demos, or durable checkpointers for horizontally scaled instances).

**Client experience.** The bundled [`interview_client.html`](interview-service/src/static/interview_client.html) and reference CV fixtures ([`SAMPLE_CV`](interview-service/src/agent/data/sample_data.py)) illustrate the flow. In production, interview context is driven by **authenticated callers** and **structured CV data** produced by the Analyze pipeline (MongoDB / integration contracts), so sessions personalize questions against the candidate profile.

**WebSocket contract.** [interview-service/src/api/v1/endpoints/interview.py](interview-service/src/api/v1/endpoints/interview.py) exposes `WS /api/v1/interview/ws/{user_id}` and delegates to [`InterviewConnectionManager`](interview-service/src/api/v1/managers/interview_manager.py).

- Client JSON `type`: `user_message` (requires `content`), `end_interview`, `get_status`; unknown types fall back to treating payload as user text.
- Server sends JSON such as `interview_started`, `agent_message` (with stage), `interview_status`, `interview_complete`, `error`.

---

## Analyze Service

**Entrypoint.** [analyze-service/src/main.py](analyze-service/src/main.py) — initializes the [dependency-injector container](analyze-service/src/containers/container.py), waits for RabbitMQ, runs `await rabbitmq_consumer.process_messages()` indefinitely.

**Configuration.** [analyze-service/src/config.py](analyze-service/src/config.py): `S3_*`, `RABBITMQ_*` (inbound job queue **`cv-analyze-stream`**; producer targets **`cv-analysis-results`** for completion events), `MONGODB_*` including `cv_analysis_collection_name`.

**Messaging topology.** Jobs arrive on **`cv-analyze-stream`**. After successful analysis, [`RabbitMQProducer`](analyze-service/src/adapters/outbound/rabbitmq_producer.py) publishes **`CVResultAnalysisMessage`** JSON to **`cv-analysis-results`** (distinct routing from the job queue), so subscribers consume outcomes without re-entering the analyzer pipeline.

**Consumer.** [analyze-service/src/adapters/inbound/rabbitmq_consumer.py](analyze-service/src/adapters/inbound/rabbitmq_consumer.py): aio-pika `connect_robust`, `prefetch_count=5`, durable queue subscription on the job queue. Incoming JSON is dispatched to [`CVAnalyzeUseCase`](analyze-service/src/use_cases/cv_analyze_use_case.py) when `message.routing_key` matches the configured analyzer queue name (`requeue=False` on failure paths inside `message.process`).

**Pipeline** ([analyze-service/src/use_cases/cv_analyze_use_case.py](analyze-service/src/use_cases/cv_analyze_use_case.py)):

1. Validate `CVInitialAnalysisMessage`.
2. Download PDF bytes from S3 using the message URL.
3. Extract text off the event loop (`asyncio.to_thread`) via [`IPDFLoader`](analyze-service/src/domain/adapters/outbound/pdf_loader.py).
4. Run [`CVAnalyzer`](analyze-service/src/agent/services/cv_analyzer.py) — LangChain structured output into [`CVData`](analyze-service/src/domain/models/cv_data.py).
5. `insert_one` into MongoDB.
6. Publish `CVResultAnalysisMessage` JSON via [`RabbitMQProducer`](analyze-service/src/adapters/outbound/rabbitmq_producer.py) to **`cv-analysis-results`**.

---

## Notification Service

**Entrypoint.** [notification-service/src/main.py](notification-service/src/main.py) — synchronous `main()`: wait for RabbitMQ, run blocking consumer, close Mongo on exit.

**Packaging.** [notification-service/pyproject.toml](notification-service/pyproject.toml) uses PEP 621 `[project]` metadata with `poetry-core` as the build backend (distinct from the pure `[tool.poetry]` style used in some sibling services).

**Configuration.** [notification-service/src/config.py](notification-service/src/config.py): RabbitMQ (`RABBITMQ_*`), MongoDB (`MONGODB_*`), SES (`SES_*`) plus AWS credentials. Mongo connection URIs **support cluster authentication modes**, including `authSource` and related parameters, via settings and client wiring aligned with your deployment.

**Consumer.** [notification-service/src/adapters/inbound/rabbitmq_consumer.py](notification-service/src/adapters/inbound/rabbitmq_consumer.py): **pika** blocking connection; durable queue **`reset-password-stream`**; `prefetch_count=5`. Successful handling `basic_ack`; failures `basic_nack(..., requeue=False)`.

**Use case.** [notification-service/src/application/use_cases/reset_password_use_case.py](notification-service/src/application/use_cases/reset_password_use_case.py): validates the inbound payload model, persists via Mongo repository context manager, retries SES send up to five attempts.

There is no `.env.example` in this service; required variables are inferred from `config.py`.

---

## Data stores

| Technology | Service | Usage |
|------------|---------|-------|
| PostgreSQL | User Management | Users table; Alembic-managed schema |
| Redis | User Management | Refresh-token rotation / reuse detection (`refresh-key:{token}`) |
| MongoDB | Analyze | CV analysis documents (`MONGODB_CV_ANALYSIS_COLLECTION_NAME`) |
| MongoDB | Notification | Outbound message records |
| S3 | Analyze | CV PDF objects (LocalStack or AWS) |
| AWS SES | Notification | Transactional email |

---

## Running the stack

Follow [README.md](README.md) “Quick start”: per-service `poetry install`, environment files where `.env.example` exists, Alembic for User Management, `uvicorn` for HTTP services, `python -m src.main` for workers, and Compose files under each service for local infra. Compose services mirror production boundaries (Postgres, Redis, RabbitMQ, MongoDB, LocalStack) for repeatable onboarding.

---
