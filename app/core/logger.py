import logging
import sys
from contextvars import ContextVar

from loguru import logger

from app.core.config import settings

correlation_id_context: ContextVar[str] = ContextVar(
    "correlation_id",
    default="-",
)


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame = logging.currentframe()
        depth = 2

        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(
            depth=depth,
            exception=record.exc_info,
        ).log(level, record.getMessage())


def _patch_record(record: dict) -> None:
    record["extra"]["correlation_id"] = correlation_id_context.get()


def configure_logging() -> None:
    logger.remove()

    logger.configure(
        patcher=_patch_record,
    )

    if settings.LOG_JSON:
        logger.add(
            sys.stdout,
            serialize=True,
            level=settings.LOG_LEVEL,
            backtrace=settings.LOG_BACKTRACE,
            diagnose=False,
        )

        return

    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        backtrace=settings.LOG_BACKTRACE,
        diagnose=False,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "{extra[correlation_id]} | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "{message} | "
            "{extra}"
        ),
    )

    intercept_handler = InterceptHandler()
    logging.root.handlers = [intercept_handler]
    logging.root.setLevel(settings.LOG_LEVEL)

    for logger_name in (
        "uvicorn.error",
        "uvicorn.access",
        "fastapi",
    ):
        logging_log = logging.getLogger(logger_name)
        logging_log.handlers = [intercept_handler]
        logging_log.propagate = False


__all__ = [
    "logger",
    "configure_logging",
    "correlation_id_context",
]
