import logging
import logging.handlers


def set_logger(module_name: object) -> object:
    """ Discordの会話ログを作成
    Discordのログを作成する。

    Args:
        module_name (str): loggerライブラリを呼び出したプロセス名。

    Returns:
        function: logger関数を返す。
    """

    logger = logging.getLogger(module_name)
    logger.handlers.clear()

    stream_handler = logging.StreamHandler()
    file_handler = logging.handlers.RotatingFileHandler('./log/bot.log', maxBytes=250000, backupCount=5)

    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] (%(module)s | %(process)d) %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger


if __name__ == '__main__':
    set_logger()
