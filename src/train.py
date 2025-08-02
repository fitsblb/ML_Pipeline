
#  Imports and Setup
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
import pickle
import yaml
import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables from .env file
load_dotenv()

# Load parameters once at module level
with open("params.yaml", "r") as file:
    params = yaml.safe_load(file)["train"]

# Get environment variables with validation
mlflow_uri = os.getenv("MLFLOW_TRACKING_URI")
mlflow_username = os.getenv("MLFLOW_TRACKING_USERNAME")
mlflow_password = os.getenv("MLFLOW_TRACKING_PASSWORD")

# Validate that credentials are loaded
if not all([mlflow_uri, mlflow_username, mlflow_password]):
    raise ValueError("Missing MLflow credentials in environment variables")

# Set environment variables
# os.environ["MLFLOW_TRACKING_URI"] = mlflow_uri
os.environ["MLFLOW_TRACKING_USERNAME"] = mlflow_username
os.environ["MLFLOW_TRACKING_PASSWORD"] = mlflow_password

def hyper_param_tunning(X_train, y_train, param_grid):
    """Perform hyperparameter tuning using GridSearchCV"""
    rf = RandomForestClassifier(random_state=params["random_state"])
    grid_search = GridSearchCV(
        estimator=rf, 
        param_grid=param_grid,
        cv=3,
        verbose=2,
        n_jobs=-1,
        scoring='accuracy'
    )
    grid_search.fit(X_train, y_train)
    return grid_search

def train():
    """Train the classifier with MLflow tracking"""
    try:
        # Load data
        data = pd.read_csv(params["data"])
        X = data.drop(columns=["Outcome"])
        y = data["Outcome"]
        
        # Set MLflow tracking
        mlflow.set_tracking_uri(mlflow_uri)
        
        with mlflow.start_run():
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, 
                test_size=0.2, 
                random_state=params["random_state"],
                stratify=y  
            )
            
            # Infer signature
            signature = infer_signature(X_train, y_train)
            
            # Log dataset info
            mlflow.log_param("train_size", len(X_train))
            mlflow.log_param("test_size", len(X_test))
            mlflow.log_param("random_state", params["random_state"])
            
            # Hyperparameter tuning
            param_grid = params["hyperparameter_grid"]
            
            print("Starting hyperparameter tuning...")
            grid_search = hyper_param_tunning(X_train, y_train, param_grid)
            
            # Get best model
            best_model = grid_search.best_estimator_
            
            # Make predictions
            y_pred = best_model.predict(X_test)
            
            # Calculate metrics
            acc_score = accuracy_score(y_test, y_pred)
            conf_matrix = confusion_matrix(y_test, y_pred)
            class_report = classification_report(y_test, y_pred)
            
            # Log metrics
            mlflow.log_metric("accuracy", acc_score)
            mlflow.log_metric("best_cv_score", grid_search.best_score_)
            
            # Log best parameters (cleaner way)
            mlflow.log_params(grid_search.best_params_)
            
            # Log confusion matrix and classification report
            mlflow.log_text(str(conf_matrix), "confusion_matrix.txt")
            mlflow.log_text(class_report, "classification_report.txt")
            
            # Check tracking URL type to handle DagHub
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
            
            if tracking_url_type_store != 'file':
                # For remote tracking (DagHub) - avoid signature issues
                mlflow.sklearn.log_model(
                    best_model, 
                    "model", 
                    registered_model_name="Diabetes_Prediction_Model",
                    input_example=X_train.iloc[:5]
                )
            else:
                # For local tracking - include signature
                mlflow.sklearn.log_model(
                    best_model, 
                    "model", 
                    signature=signature
                )
            
            # Save model locally
            model_path = Path(params["model"])
            model_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(model_path, 'wb') as f:
                pickle.dump(best_model, f)
            
            # Print results
            print(f"Accuracy score on test data: {acc_score:.4f}")
            print(f"Best parameters: {grid_search.best_params_}")
            print(f"Model saved to: {model_path}")
            print(f"Classification Report:\n{class_report}")
            
            return best_model, acc_score
            
    except Exception as e:
        print(f"Error during training: {e}")
        raise

if __name__ == "__main__":
    train()