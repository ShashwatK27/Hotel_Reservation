import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score,precision_score,f1_score,recall_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml,load_data
from scipy.stats import randint,uniform
import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class Model_Training:
  def __init__(self,train_path,test_path,model_output_path):
    self.train_path = train_path
    self.test_path = test_path
    self.output_path = model_output_path

    self.params_dist = LIGHTGBM_PARAMS
    self.random_search_param = RANDOM_SEARCH_PARAMS

  def load_and_split_data(self):
    try : 
      logger.info(f"Loading data from {self.train_path}")

      train_df = load_data(self.train_path)

      logger.info(f"Loading data from {self.test_path}")

      test_df = load_data(self.test_path)

      X_train = train_df.drop(columns = ["booking_status"])
      y_train = train_df["booking_status"]

      X_test = test_df.drop(columns = ["booking_status"])
      y_test = test_df["booking_status"]

      logger.info("Successfully split the data")

      return X_test,X_train,y_test,y_train
    
    except Exception as e:
      logger.error(f"Error while splitting data {e}")
      raise CustomException("Failed during splitting data",e)
    
  def lgbm_model(self,X_train,y_train):
    try: 
      
      logger.info("Initializing model")
      lgbm_model = lgb.LGBMClassifier(random_state=self.random_search_param['random_state'])

      logger.info("Starting Hyperparameter tuning")

      random_search = RandomizedSearchCV(
        estimator=lgbm_model,
        param_distributions=self.params_dist,
        n_iter = self.random_search_param['n_iter'],
        n_jobs = self.random_search_param['n_jobs'],
        cv = self.random_search_param['cv'],
        verbose = self.random_search_param['verbose'],
        random_state = self.random_search_param['random_state'],
        scoring = self.random_search_param['scoring']
      )

      logger.info("Starting Hyperparameter Tuning")

      random_search.fit(X_train,y_train)

      logger.info("Hyperparameter Tuning completed")

      best_params = random_search.best_params_

      best_lgbm_model = random_search.best_estimator_

      logger.info(f"Best Parameters : {best_params}")

      return best_lgbm_model
    

    except Exception as e:
      logger.error(f"Error while training model {e}")
      raise CustomException("Failed to train model",e)
    
  def evaluate_model(self, model, X_test,y_test):
    try:
      
      logger.info("starting evaluation of model")

      y_pred = model.predict(X_test)


      accuracy = accuracy_score(y_test,y_pred)
      precision = precision_score(y_test, y_pred)
      recall = recall_score(y_test,y_pred)
      f1 = f1_score(y_test,y_pred)

      logger.info(f"accuracy score : {accuracy}")
      logger.info(f"precision score : {precision}")
      logger.info(f"recall score : {recall}")
      logger.info(f"f1 score : {f1}")

      return {
        "accuracy":accuracy,
        "precision":precision,
        "recall": recall,
        "f1": f1
      }
    
    except Exception as e:
      logger.error(f"Error while Evaluating model {e}")
      raise CustomException("Failed to evaluate model",e)
    
  def save_model(self,model):
    try:
      os.makedirs(os.path.dirname(self.output_path),exist_ok=True)

      logger.info("Saving the model")

      joblib.dump(model, self.output_path)
      logger.info(f"Model saved successfully at {self.output_path}")


    except Exception as e:
      logger.error(f"Error while saving model {e}")
      raise CustomException("Failed to save model",e)

  def run(self):
    try:

      with mlflow.start_run():
        logger.info("Starting our Model Training Pipeline ")

        logger.info("starting our mlflow experimentation")

        logger.info("Logging the training and testing data")
        mlflow.log_artifact(self.train_path, artifact_path = "datasets")
        mlflow.log_artifact(self.test_path, artifact_path = "datasets")

        X_test,X_train,y_test,y_train = self.load_and_split_data()

        lgbm_model = self.lgbm_model(X_train,y_train)

        metrics = self.evaluate_model(lgbm_model,X_test,y_test)

        self.save_model(lgbm_model)

        logger.info("Logging the model into MLFLOW")
        mlflow.log_artifact(self.output_path)

        logger.info("Logging in param and metrics")
        mlflow.log_params(lgbm_model.get_params())
        mlflow.log_metrics(metrics)
        logger.info("Successfully trained the model")

    except Exception as e:
      logger.error(f"Error while training model {e}")
      raise CustomException("Failed to train model",e)
    

if __name__ == "__main__":
  trainer = Model_Training(TRAIN_PROCESSED_PATH,TEST_PROCESSED_PATH,MODEL_OUTPUT_PATH)
  trainer.run()

