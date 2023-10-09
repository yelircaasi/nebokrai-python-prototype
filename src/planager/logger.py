from logging import Logger


def get_logger() -> Logger:
    logger = Logger("planager")
    return logger


# logger = get_logger(config)
