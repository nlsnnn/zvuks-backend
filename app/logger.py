from loguru import logger


def setup_logger(name: str = "app") -> None:
    logger.remove()
    logger.add(
        f"logs/{name}_{{time:YYYY-MM-DD}}.log", rotation="1 day", retention="7 days", level="INFO"
    )
