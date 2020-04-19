import sys, os
import logging
logger = logging.getLogger(__name__)


def exception_handler(exception, file=None):
    if file:
        logger.error(f'{os.path.splitext(os.path.basename(file))[0]} - {exception}')
    else:
        logger.error(exception)
    sys.exit(1)