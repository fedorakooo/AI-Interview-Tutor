from abc import ABC, abstractmethod


class IRabbitMQConsumer(ABC):
    """Interface defining message broker consumer operations."""

    @abstractmethod
    async def process_messages(self) -> None:
        """Processes messages received from the broker."""
        pass
