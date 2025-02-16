# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies and debugging tools
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    git \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy debugging scripts
COPY debug_deployment.sh ./

# Make the debug script executable
RUN chmod +x debug_deployment.sh

# Copy only the requirements file
COPY src/requirements.txt ./

# Verbose pip installation with extensive logging
RUN pip install --no-cache-dir --verbose \
    --upgrade pip setuptools wheel \
    && pip install --no-cache-dir --verbose -r requirements.txt \
    || (echo "PIP INSTALLATION FAILED" && cat requirements.txt && pip freeze && exit 1)

# Copy the rest of the application
COPY src/ ./

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Debugging environment variables
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_VERBOSE=1

# Run debugging script or the application
CMD ["/bin/bash", "-c", "./debug_deployment.sh || gunicorn --bind 0.0.0.0:5000 app:app"]
