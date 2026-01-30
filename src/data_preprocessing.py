import os 
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from utils.common_functions import read_yaml,load_data
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from config.paths_config import *

logger = get_logger(__name__)


class DataProcessor:
  def __init__(self, train_path,test_path,processed_dir,config_path):
    self.train_path = train_path
    self.test_path = test_path
    self.process_dir = processed_dir

    self.config = read_yaml(config_path)

    if not os.path.exists(self.process_dir):
      os.makedirs(self.process_dir)
    

  def preprocess_data(self,df):
    try:
      logger.info("starting preprocessing of our dataset")

      logger.info("Dropping Columns")
      df.drop(columns=['Unnamed: 0', 'Booking_ID'],inplace = True)
      df.drop_duplicates(inplace=True)

      cat_cols = self.config["data preprocessing"]["categorical_columns"]
      num_cols = self.config["data preprocessing"]["numerical_columns"]

      logger.info("Applying Label Encoding")

      mappings={}

      le=LabelEncoder()
      for col in cat_cols:
          df[col]=le.fit_transform(df[col])

          mappings[col]= {label:code for label, code in zip(le.classes_, le.transform(le.classes_))}

      logger.info("Label Encodings are:")
      for col,mappings in mappings.items():
        logger.info(f"{col} : {mappings}")


      logger.info("Handling Skewness")

      skew_threshold = self.config["data preprocessing"]["skewness_threshold"]
      skewness = df[num_cols].apply(lambda x:x.skew())


      for columns in skewness[skewness>skew_threshold].index:
        df[columns] = np.log1p(df[columns])

      return df
    
    except Exception as e:
       logger.error(f"Error during preprocess step {e}")
       raise CustomException("Error while preprocess data",e)
    

  def imbalanced_data(self,df):
    try:
      logger.info("Handling Imbalanced data")

      X = df.drop('booking_status', axis=1)
      y= df['booking_status']

      smote = SMOTE(random_state=42)
      X_resampled, y_resampled = smote.fit_resample(X, y)

      balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
      balanced_df['booking_status'] = y_resampled

      logger.info("Successfully balanced data")
      return balanced_df
    
    except Exception as e:
      logger.error(f"Failed to balance data {e}")
      raise CustomException("Error while balancing data")
    
  def feature_selection(self,df):
    try:
      logger.info("Starting best feature selection")
      X = df.drop('booking_status', axis=1)
      y = df['booking_status']

      classifier = RandomForestClassifier(random_state=42)
      classifier.fit(X, y)

      feature_importance=classifier.feature_importances_

      feature_importance_df = pd.DataFrame({
            'feature': X.columns,
            'importance': feature_importance
          })
      
      top_features = feature_importance_df.sort_values(by='importance', ascending=False)

      num_features_to_select = self.config["data preprocessing"]["num_feature"]

      top_10_features = top_features['feature'].head(num_features_to_select).values
      top_10_features_df = df[top_10_features.tolist()+['booking_status']]

      logger.info("Best features selected")
      return top_10_features_df
    
    except Exception as e:
      logger.error(f"Failed to get best features {e}")
      raise CustomException("Error while getting best features ",e)
    
  def save_data(self,df,file_path):
    try:
      logger.info("Starting to save data")
      df.to_csv(file_path, index=False)
      logger.info(f"Data saved succesfully at {file_path}")

    except Exception as e:
      logger.error(f"error while saving data {e}")
      raise CustomException("Failed to save data",e)
    

  def process(self):
    try:
      logger.info("Starting to process the data")

      train_df = load_data(self.train_path)
      test_df = load_data(self.test_path)

      train_df = self.preprocess_data(train_df)
      test_df = self.preprocess_data(test_df)

      train_df = self.imbalanced_data(train_df)
      test_df = self.imbalanced_data(test_df)

      train_df = self.feature_selection(train_df)
      test_df = test_df[train_df.columns]

      self.save_data(train_df,TRAIN_PROCESSED_PATH)
      self.save_data(test_df, TEST_PROCESSED_PATH)

    except Exception as e:
      logger.error(f"Error while preprocessing data {e}")
      raise CustomException("Failed to preprocess data",e)
    

if __name__ == "__main__":
  preprocessor = DataProcessor(TRAIN_FILE_path,TEST_FILE_path,PROCESSED_DIR,CONFIG_FILE_PATH)
  preprocessor.process()




