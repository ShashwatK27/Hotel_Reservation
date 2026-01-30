from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import  Model_Training
from config.paths_config import *
from utils.common_functions import read_yaml



if __name__ == "__main__":
  data_ingestion= DataIngestion(read_yaml(CONFIG_FILE_PATH))
  data_ingestion.run()

  preprocessor = DataProcessor(TRAIN_FILE_path,TEST_FILE_path,PROCESSED_DIR,CONFIG_FILE_PATH)
  preprocessor.process()

  trainer = Model_Training(TRAIN_PROCESSED_PATH,TEST_PROCESSED_PATH,MODEL_OUTPUT_PATH)
  trainer.run()