import logging.config

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.containers.agent import AgentContainer
from src.containers.inbound_adapter import InboundAdaptersContainer
from src.containers.outbound_adapter import OutboundAdaptersContainer
from src.containers.use_cases import UseCasesContainer


class Container(DeclarativeContainer):
    yaml_config = providers.Configuration(yaml_files=["config.yaml"])

    logging_config = providers.Resource(logging.config.dictConfig, config=yaml_config.logger)

    app_logger = providers.Singleton(logging.getLogger, name="app")

    agent_logger = providers.Singleton(logging.getLogger, name="agent")

    outbound_adapters = providers.Container(
        OutboundAdaptersContainer,
        logger=app_logger,
    )

    agent = providers.Container(
        AgentContainer,
        logger=agent_logger,
    )

    use_cases = providers.Container(
        UseCasesContainer,
        outbound_adapters=outbound_adapters,
        agent=agent,
    )

    inbound_adapters = providers.Container(InboundAdaptersContainer, logger=app_logger, use_cases=use_cases)
