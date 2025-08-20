import asyncio
import socket
import time
from logging import Logger

from dependency_injector.wiring import Provide, inject

from src.config import settings
from src.containers.container import Container
from src.use_cases.cv_analyze_use_case import CVAnalyzeUseCase


@inject
def wait_for_rabbitmq(
    host: str = settings.rabbitmq_settings.host,
    port: int = settings.rabbitmq_settings.port,
    timeout: float = settings.rabbitmq_settings.timeout,
    logger: Logger = Provide[Container.app_logger],
) -> None:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1.0):
                logger.info("RabbitMQ connection established")
                return
        except Exception:
            time.sleep(1.0)
            logger.info("Waiting for RabbitMQ connection")

    raise TimeoutError("RabbitMQ connection timed out")


@inject
async def main(use_case: CVAnalyzeUseCase = Provide[Container.use_cases.cv_analyze_use_case]):
    wait_for_rabbitmq()
    await use_case("CV.pdf")


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])

    container.init_resources()

    asyncio.run(main())
