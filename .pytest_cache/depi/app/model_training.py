import os
import mlflow
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, GridSearchCV
import matplotlib
import matplotlib.pyplot as plt
import warnings
from sklearn.exceptions import ConvergenceWarning

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module="mlflow.*")
warnings.filterwarnings("ignore", category=ConvergenceWarning)

# Set a non-interactive backend for Matplotlib
matplotlib.use('Agg')  # Prevent interactive plot windows

# Set MLflow Tracking URI
mlflow.set_tracking_uri("file:///mlflow_logs")


# Function to set up MLflow experiment
def set_mlflow_experiment(experiment_name):
    mlflow.set_experiment(experiment_name)


# Data preparation for classification (binary target)
def prepare_data_classification(data):
    # Create a binary target for high rentals (e.g., `cnt` > 500)
    data['high_rentals'] = (data['cnt'] > 500).astype(int)

    # Select relevant features
    X = data[['season', 'temp', 'hum', 'windspeed']]  # Features
    y = data['high_rentals']  # Target variable

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

    return X_train, X_test, y_train, y_test


# Data preparation for regression (continuous target)
def prepare_data_regression(data):
    # Select relevant features
    X = data[['season', 'temp', 'hum', 'windspeed']]  # Features
    y = data['cnt']  # Target variable

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train, X_test, y_test, task="classification"):
    with mlflow.start_run():
        if task == "classification":
            # Hyperparameter tuning for Logistic Regression
            param_grid = {'C': [0.1, 1, 10]}
            grid = GridSearchCV(LogisticRegression(), param_grid, cv=5)
            grid.fit(X_train, y_train)

            best_model = grid.best_estimator_
            mlflow.log_param("best_C", grid.best_params_['C'])

            # Make predictions
            y_pred = best_model.predict(X_test)
            y_pred_proba = best_model.predict_proba(X_test)[:, 1]

            # Evaluate the model
            metrics = classification_report(y_test, y_pred, output_dict=True)
            print(confusion_matrix(y_test, y_pred))

            # Log metrics
            mlflow.log_metric("accuracy", metrics["accuracy"])
            mlflow.log_metric("precision", metrics["1"]["precision"])
            mlflow.log_metric("recall", metrics["1"]["recall"])
            mlflow.log_metric("f1-score", metrics["1"]["f1-score"])

            # Log AUC-ROC
            auc = roc_auc_score(y_test, y_pred_proba)
            mlflow.log_metric("roc_auc", auc)

            # Save and log ROC curve
            fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
            plt.figure()
            plt.plot(fpr, tpr, color='blue', label='ROC curve (area = %0.2f)' % auc)
            plt.plot([0, 1], [0, 1], color='red', linestyle='--')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('Receiver Operating Characteristic')
            plt.legend(loc='lower right')
            plt.savefig("roc_curve.png")
            mlflow.log_artifact("roc_curve.png")

        elif task == "regression":
            # Train a Linear Regression model
            from sklearn.linear_model import LinearRegression
            best_model = LinearRegression()
            best_model.fit(X_train, y_train)

            # Make predictions
            y_pred = best_model.predict(X_test)

            # Evaluate the model
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            print(f"Mean Squared Error: {mse}")
            print(f"R2 Score: {r2}")

            # Log metrics
            mlflow.log_metric("mse", mse)
            mlflow.log_metric("r2_score", r2)

        # Log the trained model
        mlflow.sklearn.log_model(best_model, "model")

        return best_model


def main_train_model(task="classification"):
    try:
        set_mlflow_experiment("Bike Sharing Experiment")  # Set your desired experiment name

        # Use `day.csv` for daily analysis
        data_file = r"C:\Users\walee\Downloads\Depi\Depi\database\bike+sharing+dataset\day.csv"

        if not os.path.exists(data_file):
            raise FileNotFoundError(f"Dataset not found at: {data_file}")

        data = pd.read_csv(data_file)
        print(f"Data shape: {data.shape}")

        # Check task type and prepare data
        if task == "classification":
            X_train, X_test, y_train, y_test = prepare_data_classification(data)
        elif task == "regression":
            X_train, X_test, y_train, y_test = prepare_data_regression(data)
        else:
            raise ValueError("Invalid task. Choose 'classification' or 'regression'.")

        # Train the model
        model = train_model(X_train, y_train, X_test, y_test, task=task)
        print("Model training completed successfully.")
        return model
    except Exception as e:
        print("An error occurred:", e)


# Run the script
if __name__ == "__main__":
    # Change task to "regression" if you want to predict bike counts (cnt)
    model = main_train_model(task="classification")
