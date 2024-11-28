import mlflow
client = mlflow.tracking.MlflowClient()
client.get_latest_versions("depi_default_prediction")
