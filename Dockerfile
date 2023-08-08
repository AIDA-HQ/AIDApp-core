# Use an official Python 3.10 runtime as a parent image
FROM ghcr.io/aida-hq/python-gunicorn-uvicorn-docker:py3.10-slim-LATEST

# Copy the requirements file into the container
COPY ./requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Export environment variables
ENV APP_MODULE="aidapp.api.main:app" 

# Copy the rest of the application code into the container
COPY ./src .
