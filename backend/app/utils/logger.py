import os
from loguru import logger


def setup_logger() -> None:
    os.makedirs("outputs/logs", exist_ok=True)
    logger.remove()
    logger.add(
        "outputs/logs/app.log",
        rotation="1 MB",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )
    logger.add(
        lambda msg: print(msg, end=""),
        level="INFO",
        format="{time:HH:mm:ss} | {level} | {message}"
    )


def log_event(agent: str, message: str) -> str:
    log_message = f"[{agent}] {message}"
    logger.info(log_message)
    return log_message