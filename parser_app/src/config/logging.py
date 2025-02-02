import logging

ai_logger = logging.getLogger("ai_logger")
ai_logger.setLevel(logging.INFO)

ai_handler = logging.FileHandler("ai.log")
ai_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] [AI] %(message)s",
)
ai_handler.setFormatter(ai_formatter)
ai_logger.addHandler(ai_handler)

main_logger = logging.getLogger("main_logger")
main_logger.setLevel(logging.INFO)

main_handler = logging.FileHandler("parser.log")
main_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
main_handler.setFormatter(main_formatter)
main_logger.addHandler(main_handler)


def setup_logging() -> tuple[logging.Logger, logging.Logger]:
    return main_logger, ai_logger
