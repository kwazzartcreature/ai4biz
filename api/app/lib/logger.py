import logging
from .config import LOGGING_LEVEL


logging.basicConfig(format="%(levelname)s:%(message)s", level=LOGGING_LEVEL)
