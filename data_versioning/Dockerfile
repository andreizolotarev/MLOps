# base image
FROM python:3.7-slim

# define user and group
ARG USER_ID
ARG GROUP_ID

# copy required libraries
COPY ./requirements.txt ./

# install required libraries
RUN apt update && apt -y upgrade && \
    pip install -r ./requirements.txt && \
    apt -y install git

# create a new user with group
RUN addgroup --gid $GROUP_ID new_user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID new_user

# switch to a new user
USER new_user

# select working directory
WORKDIR /home/new_user


