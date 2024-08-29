# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory   

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY . /app/

# Expose the application port (adjust as needed)
EXPOSE 9000

# Define the command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]