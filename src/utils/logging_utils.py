import logging
import tqdm


class TqdmLoggingHandler(logging.Handler):
    """
    Logging Handler for tqdm.
    From https://stackoverflow.com/questions/38543506/change-logging-print-function-to-tqdm-write-so-logging-doesnt-interfere-wit
    """

    def __init__(self, level=logging.NOTSET):
        super(self.__class__, self).__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.tqdm.write(msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def get_logger(level: str) -> logging.Logger:
    """
    Return a logger able to display information with tqdm progress bars.
    :param level: logging level
    :return: the logger object
    """
    logger = logging.getLogger()

    tqdm_logging_handler = TqdmLoggingHandler()
    tqdm_logging_handler.setFormatter(logging.Formatter(fmt="[%(asctime)s][%(levelname)s] %(message)s"))

    logger.addHandler(tqdm_logging_handler)
    logger.setLevel(getattr(logging, level))

    return logger
