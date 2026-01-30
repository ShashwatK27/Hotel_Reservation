import os 
import pandas as pd
from sklearn.model_selection import train_test_split
from google.cloud import storage
from src.logger import get_logger
from src.custom_exception import CustomException
from utils.common_functions import read_yaml
from config.paths_config import *

logger = get_logger(__name__)

class DataIngestion:
  def __init__(self,config):
    self.config=config["data_ingestion"]
    self.bucket_name=self.config["bucket_name"]
    self.file_name=self.config["bucket_file_name"]
    self.train_test_ratio=self.config["train_ratio"]

    os.makedirs(RAW_DIR, exist_ok=True)

    logger.info("DataIngestion instance created.")

  def download_csv_from_gcp(self):
    try:
      client = storage.Client()
      bucket = client.bucket(self.bucket_name)
      blob = bucket.blob(self.file_name)

      blob.download_to_filename(RAW_FILE_path)

      logger.info(f"File {self.file_name} downloaded from bucket {self.bucket_name} to {RAW_FILE_path}.")

    except Exception as e:
      logger.error(f"Error downloading file from GCP: {e}")
      raise CustomException("Failed to download file from GCP", e)
    
  def split_data_as_train_test(self):
    try: 
      logger.info("Starting data split into train and test sets.")
      df= pd.read_csv(RAW_FILE_path)
      train_data,test_data = train_test_split(df, test_size= 1 - self.train_test_ratio, random_state=42)

      train_data.to_csv(TRAIN_FILE_path)
      test_data.to_csv(TEST_FILE_path)

      logger.info(f"train data saved at: {TRAIN_FILE_path} and test data saved at: {TEST_FILE_path}")

    except Exception as e:
      logger.error(f"Error during train-test split: {e}")
      raise CustomException("Failed to split data into train and test sets", e)
    
  def run(self):
    try:
      self.download_csv_from_gcp()
      self.split_data_as_train_test()
    except Exception as e:
      logger.error(f"Error in data ingestion run method: {e}")
      raise CustomException("Data ingestion process failed", e)
    finally:
      logger.info("Data ingestion process completed.")

if __name__ == "__main__":
  data_ingestion= DataIngestion(read_yaml(CONFIG_FILE_PATH))
  data_ingestion.run()