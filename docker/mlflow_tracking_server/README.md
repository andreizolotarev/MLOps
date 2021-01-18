# MLFLOW
## In this example a docker container will be built for using Mlflow as a tracking server
## CLI

1) Build an image with human readable name:  
```
docker build -t mlflow_image --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .
```
2) Run a container (Start Mlflow's servevr at port 7777):  
```
docker run -d -v $(pwd)/volume:/home/new_user/volume -p 7777:7777 --name mlflow_container mlflow_image
```
If you go to 0.0.0.0:7777, then you will see mlflow UI


