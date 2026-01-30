import logging
import os

from datetime import datetime 

LOG_DIRS = "logs"

os.makedirs(LOG_DIRS,exist_ok=True)

LOG_FILE = os.path.join(LOG_DIRS, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

logging.basicConfig(
    filename=LOG_FILE,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    level= logging.INFO,
)

def get_logger(__name__):
  logger= logging.getLogger(__name__)
  logger.setLevel(logging.INFO)
  return logger