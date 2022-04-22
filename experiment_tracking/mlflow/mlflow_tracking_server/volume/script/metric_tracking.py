import os
import mlflow
from random import random, randint

if __name__ == "__main__":
    mlflow.set_tracking_uri("http://mlflow_server:7777")
    mlflow.set_experiment("my-experiment")
    with mlflow.start_run():
        # Log a parameter (key-value pair)
        mlflow.log_param("param1", randint(0, 100))

        # Log a metric; metrics can be updated throughout the run
        mlflow.log_metric("foo", random())
        mlflow.log_metric("foo", random() + 1)
        mlflow.log_metric("foo", random() + 2)
