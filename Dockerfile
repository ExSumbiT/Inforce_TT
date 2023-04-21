# Use the official Python image as a base image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the project files into the container
COPY lunch_decision .

# Expose the port the app runs on
EXPOSE 8000

COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh