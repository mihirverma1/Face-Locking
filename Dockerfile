# Use Ubuntu as the base image
FROM ubuntu:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and necessary tools
RUN apt-get update && apt-get install -y python3 python3-pip python3-opencv && apt-get clean

# Create a non-root user and group
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Set the working directory in the container
WORKDIR /app

# Copy the local project files to the container
COPY . /app

# Change ownership of the working directory to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose any required ports (optional, depending on your project)
EXPOSE 8888

# Default command to run your application
CMD ["python3", "app.py"]