import logging.config

from src.config import settings

logging.config.dictConfig(settings.logger_settings.LOGGING_CONFIG)

logger = logging.getLogger("app")
