# Use the Python base image
FROM python:3.10-alpine
# Set the working directory
WORKDIR /app
# Copy the backend code into the container
COPY . /app
# Install virtualenv
RUN pip install virtualenv
# Create a virtual environment
RUN virtualenv venv
# Activate the virtual environment
RUN source venv/bin/activate
# Install dependencies
RUN pip install -r requirements.txt
# Set the command to run when the container starts
CMD ["/bin/sh", "-c", "gunicorn -w 4 --bind 0.0.0.0:5000 api:app"]

##commands to build and run the container
# podman build -t chkoutmanager .
# podman run -p 5000:5000 chkoutmanager 

#save the image to local and upload.
#podman save chkoutmanager -o chkoutmanager.tar
#podman push chkoutmanager.tar url