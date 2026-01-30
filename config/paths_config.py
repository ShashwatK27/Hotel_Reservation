import os


######################## DATA INGESTION CONFIGURATION ########################

RAW_DIR= "artifacts/raw"

RAW_FILE_path = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILE_path = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_path = os.path.join(RAW_DIR, "test.csv")

CONFIG_FILE_PATH = "config/config.yaml"


######################## DATA PREPROCESSING ##################################

PROCESSED_DIR = "artifacts/processed"
TRAIN_PROCESSED_PATH = os.path.join(PROCESSED_DIR, "train_processsed.csv")
TEST_PROCESSED_PATH = os.path.join(PROCESSED_DIR, "test_processed.csv")



######################### MODEL TRAINING ####################################

MODEL_OUTPUT_PATH = "artifacts/model/lgbm_model.pkl"
