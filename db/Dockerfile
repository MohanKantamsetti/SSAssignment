#db file for mongodb container
# Use the MongoDB base image
FROM mongo:latest
#set working directory
WORKDIR /app
# Set environment variables for MongoDB
ENV MONGO_INITDB_ROOT_USERNAME=chkoutmanager_admin
ENV MONGO_INITDB_ROOT_PASSWORD=chk0ut3aNag3r_d8_4dm1n
ENV MONGO_INITDB_DATABASE=checkout_db
#Copy the db file into the container
COPY /import-files /import-files

# Copy the initialization script to the container
COPY setup.sh /docker-entrypoint-initdb.d/

#Expose the port
EXPOSE 27017

#commands to build and run the container
# podman build -t chkoutmanagerdb .
# podman run -p 27018:27018 chkoutmanagerdb

#connection string
#mongodb://chkoutmanager_admin:chk0ut3aNag3r_d8_4dm1n@localhost:27018/checkout_db