import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def get_logger(
    name: str,
    log_dir: str = "logs",
    level: int = logging.INFO,
    max_bytes: int = 5_000_000,  # 5 MB
    backup_count: int = 5
) -> logging.Logger:

    logger = logging.getLogger(name)

    # Evita duplicar handlers si se importa muchas veces
    if logger.handlers:
        return logger

    logger.setLevel(level)

    log_file = "crawler.log"

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler de archivo (rotativo)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # Handler de consola (útil mientras desarrollás)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger