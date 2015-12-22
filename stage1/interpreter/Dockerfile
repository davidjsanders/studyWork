#
# Dockerfile
# ----------
# Purpose - build the Docker container image for the microservice interpreter.
# MAINTAINER David Sanders <dsanders_can@outlook.com>
# Created - 22 Dec 2015
# Last Up - 22 Dec 2015
#
#
# Use the base Python image which includes Python3, Flask, Flask_Restful, and
# 
FROM dsanderscan/pythonbase
#
# Setup cmd2
#
RUN flask/bin/pip install cmd2
#
# Setup hosts
#
#RUN sudo echo "192.168.0.210    dasanderUty01" >> /etc/hosts
#
# Create the /interpreter directory
RUN mkdir /interpreter
RUN mkdir /interpreter/schemas
RUN mkdir /interpreter/bin
#
# copy the files required for the application
#
COPY interpreter.py /interpreter/
COPY Links.py /interpreter/
COPY Methods.py /interpreter/
COPY Parameters.py /interpreter/
COPY Response.py /interpreter/
COPY Routes.py /interpreter/
COPY Server.py /interpreter/
COPY Utilities.py /interpreter/
COPY schemas/ /interpreter/schemas/
COPY schemas/links.json /interpreter/schemas/
COPY bin/start.sh /interpreter/bin/
#
# Set the working directory for the container
#
WORKDIR /interpreter/
