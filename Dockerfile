# # Use an official Python runtime as a parent image
# FROM python:3.8-slim-buster

# # Set the working directory in the container to /app
# WORKDIR /app

# # Add the current directory contents into the container at /app
# ADD . /app

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Set the FLASK_APP environment variable
# ENV FLASK_APP=server.py

# # Change the working directory to /app/core
# WORKDIR /app/core

# # Run the database upgrade command
# RUN flask db upgrade -d migrations

# # Make port 8080 available to the world outside this container
# EXPOSE 8080

# # Run server.py when the container launches
# CMD ["python", "server.py"]

# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Add a script to be executed every time the container starts
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Run the command to start uWSGI
ENTRYPOINT ["./start.sh"]






