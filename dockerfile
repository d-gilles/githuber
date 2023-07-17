FROM python:3.10.0-slim-buster

ARG GITHUB_TOKEN
ENV GITHUB_TOKEN=${GITHUB_TOKEN}
ENV REPO_NAME=githuber

# Create a non-root
RUN useradd --create-home githuber

# Create directories and set permissions
WORKDIR /app

# Update and install dependencies
RUN pip install --upgrade pip \
    && apt-get update \
    && apt-get install -y build-essential


# Copy necessary files
COPY githuber.py /app/githuber.py
COPY requirements.txt /app/requirements.txt

# Change user
USER githuber

# Install Python requirements
RUN pip install -r requirements.txt && pip uninstall -y PyGithub && pip install PyGithub

# Specify the command to run
ENTRYPOINT ["python3", "githuber.py"]


# starte das image mit dem github key als eviroment variable
# docker build --build-arg Github_KEY=<Your Github Key> -t Githuber:latest .
