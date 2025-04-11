# Base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the dependencies file to the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files to the container
COPY . .

# Expose the desired port
EXPOSE 8080

# Set the environment variable to include the project directory in PYTHONPATH
ENV PYTHONPATH=/app

# Run Gunicorn to start the application on port 8080
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "--access-logfile", "-", "frontend.app:app"]
