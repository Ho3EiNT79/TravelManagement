import logging
from logging.handlers import RotatingFileHandler


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("out.log", maxBytes=5000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

def logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
