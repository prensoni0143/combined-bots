import logging


def setup():
    log_format = logging.Formatter(
        '%(asctime)s - [%(name)s] - [%(levelname)s] - %(message)s')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.getLogger('telethon').setLevel(logging.INFO)

    file_logger = logging.FileHandler("bot5.log", encoding="utf-8")
    file_logger.setLevel(logging.INFO)
    file_logger.setFormatter(log_format)
    logger.addHandler(file_logger)

    console_logger = logging.StreamHandler()
    console_logger.setFormatter(log_format)
    console_logger.setLevel(logging.INFO)
    logger.addHandler(console_logger)