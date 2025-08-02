import pandas as pd
import pickle
import yaml
import os
import mlflow  
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables from .env file
load_dotenv()

# Load parameters once at module level
with open("params.yaml", "r") as file:
    params = yaml.safe_load(file)["train"]

# Get (Read) environment variables with validation
mlflow_uri = os.getenv("MLFLOW_TRACKING_URI")
mlflow_username = os.getenv("MLFLOW_TRACKING_USERNAME")
mlflow_password = os.getenv("MLFLOW_TRACKING_PASSWORD")

# Validate that credentials are loaded
if not all([mlflow_uri, mlflow_username, mlflow_password]):
    raise ValueError("Missing MLflow credentials in environment variables")

# Set environment variables
os.environ["MLFLOW_TRACKING_USERNAME"] = mlflow_username
os.environ["MLFLOW_TRACKING_PASSWORD"] = mlflow_password

def evaluate(data_path, model_path):
    """Evaluate the trained model on the dataset"""
    try:
        # Load data
        data = pd.read_csv(data_path)
        X = data.drop(columns=['Outcome'])
        y = data['Outcome']

        # Set MLflow tracking
        mlflow.set_tracking_uri(mlflow_uri)
            
        with mlflow.start_run():
            # ✅ Load model correctly
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            # Make predictions
            predictions = model.predict(X)
            
            # Calculate metrics
            accuracy = accuracy_score(y, predictions)
            conf_matrix = confusion_matrix(y, predictions)
            class_report = classification_report(y, predictions)
            
            print(f"The accuracy on the data is {accuracy:.4f}")
            print(f"Confusion Matrix:\n{conf_matrix}")
            print(f"Classification Report:\n{class_report}")

            # Log metrics 
            mlflow.log_metric('accuracy', accuracy)
            
            # Log additional artifacts
            mlflow.log_text(str(conf_matrix), "confusion_matrix.txt")
            mlflow.log_text(class_report, "classification_report.txt")
            
            return accuracy
            
    except Exception as e:
        print(f"Error during evaluation: {e}")
        raise

# Execute the app
if __name__ == '__main__':
    evaluate(params['data'], params['model'])