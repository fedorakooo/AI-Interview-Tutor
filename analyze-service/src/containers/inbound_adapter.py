from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer, Dependency, Factory

from src.adapters.inbound.rabbitmq_consumer import RabbitMQConsumer
from src.config import settings
from src.domain.adapters.inbound.rabbitmq_consumer import IRabbitMQConsumer


class InboundAdaptersContainer(DeclarativeContainer):
    logger = Dependency()

    use_cases = DependenciesContainer()

    rabbitmq_consumer: IRabbitMQConsumer = Factory(
        RabbitMQConsumer,
        amqp_url=settings.rabbitmq_settings.url,
        logger=logger,
        cv_analyze_use_case=use_cases.cv_analyze_use_case,
    )
