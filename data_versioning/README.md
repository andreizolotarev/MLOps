# DVC In progress
## In this example a docker container will be built for using DVC as a data versioning tool
## CLI

1) Build an image with human readable name:  
```
docker build -t dvc_image --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .
```
2) Run a container:  
```
docker run -it -v $(pwd)/volume:/home/new_user/volume --name dvc_container dvc_image bash
```