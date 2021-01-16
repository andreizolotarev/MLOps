## In this example a docker container will be built for creating embeddings using Starspace
## A new user will be created to avoid bad practice usage of root user. Also, a volume folder with an input file will be mounted.
## CLI

1) Build an image with human readable name:  
```
docker build -t starspace_image --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .
```
2) Run a container:  
```
docker run -v $(pwd)/volume:/home/new_user/volume starspace_image
```

If you want to run a container in -it mode with bash only:
```
docker run -it -v $(pwd)/volume:/home/new_user/volume starspace_image /bin/bash
```
