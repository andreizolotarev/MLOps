FROM puckel/docker-airflow:1.10.8

USER root
RUN apt update && apt -y upgrade && \
    apt clean && rm -rf /var/lib/apt/lists/*

USER airflow
COPY ./requirements.txt ./
RUN pip install --user -r ./requirements.txt

