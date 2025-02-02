import logging
from logging.handlers import RotatingFileHandler

ai_logger = logging.getLogger("ai_logger")
ai_logger.setLevel(logging.INFO)

ai_handler = RotatingFileHandler(
    "ai.log", maxBytes=10 * 1024 * 1024, backupCount=5
)
ai_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] [AI] %(message)s",
)
ai_handler.setFormatter(ai_formatter)
ai_logger.addHandler(ai_handler)

ai_console_handler = logging.StreamHandler()
ai_console_handler.setFormatter(ai_formatter)
ai_logger.addHandler(ai_console_handler)

main_logger = logging.getLogger("main_logger")
main_logger.setLevel(logging.INFO)

main_handler = RotatingFileHandler(
    "parser.log", maxBytes=10 * 1024 * 1024, backupCount=5
)
main_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] [%(module)s:%(lineno)s] %(message)s"
)
main_handler.setFormatter(main_formatter)
main_logger.addHandler(main_handler)

main_console_handler = logging.StreamHandler()
main_console_handler.setFormatter(main_formatter)
main_logger.addHandler(main_console_handler)


def setup_logging() -> tuple[logging.Logger, logging.Logger]:
    return main_logger, ai_logger
