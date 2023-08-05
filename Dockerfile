# Use an official Python 3.10 runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY ./src .

# Expose the port that the backend server listens on
EXPOSE 8000

# Start the backend server
CMD ["uvicorn", "aidapp.api.main:app", "--host", "0.0.0.0", "--port", "80"]
