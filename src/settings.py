from loguru import logger

logger.add(
    "log.json",
    format="{time} {level} {message}",
    level="DEBUG"
)