#
# Dockerfile
# ----------
# Purpose - build the Docker container image for the Location Service
#           to enable the application to run on any platform that
#           supports Docker.
#
# MAINTAINER David Sanders <dsanders_can@outlook.com>
#
# Revision History
# -----------------------------------------------------------------------------
# Date         | By             | Reason
# -----------------------------------------------------------------------------
# 24 Jan 2015  | D Sanders      | First version.
#
#
# Use the base Python image which includes Python3, Flask, Flask_Restful, and
# 
FROM dsanderscan/pythonbase
#
# Install additional apps for this module
#
# Install Redis
#
RUN apt-get install -y redis-server
#
# Install the python Redis module
#
RUN /flask/bin/pip install redis
#
# Create the directory structures
RUN mkdir /Logger
RUN mkdir /Logger/Logger
RUN mkdir /Logger/Logger_Boundary
#
# copy the files required for the application
#
COPY runserver.py /Logger/
COPY startup.sh /Logger/
COPY Logger/__init__.py /Logger/Logger/
COPY Logger/main.py /Logger/Logger/
COPY Logger/Control.py /Logger/Logger/
COPY Logger/Log_Control.py /Logger/Logger/
COPY Logger/Logger_Database.py /Logger/Logger/
COPY Logger/Logging_Processor.py /Logger/Logger
COPY Logger_Boundary/__init__.py /Logger/Logger_Boundary/
COPY Logger_Boundary/main.py /Logger/Logger_Boundary/
COPY Logger_Boundary/Log_Boundary.py /Logger/Logger_Boundary/
#
# Set the working directory for the container
#
WORKDIR /Logger/
