# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the container
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the port used by your FastAPI application
EXPOSE 8001

# Create a startup script
RUN echo '#!/bin/bash' > /start.sh && \
    echo 'python main.py &' >> /start.sh && \
    echo 'uvicorn api:app --host 0.0.0.0 --port 8001' >> /start.sh && \
    chmod +x /start.sh

# Set the entry point to run the startup script
ENTRYPOINT ["/start.sh"]
