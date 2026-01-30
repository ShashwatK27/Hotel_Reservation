from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

def divide(a,b):
  try:
    logger.info(f"Dividing {a} by {b}")
    return a / b
  except Exception as e:
    raise CustomException("Division by zero error", sys) from e

if __name__ == "__main__":
  try:
    logger.info("Starting division operation")
    result = divide(10, 0)
  except CustomException as ce:
    logger.error(ce)