# Use the Python base image
FROM python:3.10-alpine

# Set the working directory
WORKDIR /app

# Copy the backend code into the container
COPY . /app

# Install dependencies directly without virtualenv (since it's a standalone script)
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the consumer script when the container starts
CMD ["python", "email_serve.py"]