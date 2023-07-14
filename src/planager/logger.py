from logging import Logger

from .config import ConfigType, config


def get_logger(cfg: ConfigType) -> Logger:
    logger = Logger("planager")
    return logger


logger = get_logger(config)
