#
# Dockerfile
# ----------
# Purpose - build the Docker container image for the phone screen.
# MAINTAINER David Sanders <dsanders_can@outlook.com>
# Created - 01 Feb 2016
#
#
# Use the base Python image which includes Python3, Flask, Flask_Restful, and
# 
FROM dsanderscan/pythonbase
#
# Setup hosts
#
RUN echo "192.168.0.210    dasanderUty01" >> /etc/hosts
#
# Install Redis
#
RUN apt-get install -y redis-server
#
# Install the python Redis module
#
RUN /flask/bin/pip install redis
#
# Create the /interpreter directory
RUN mkdir /Phone_Screen
#
# copy the files required for the application
#
COPY Phone_Screen.py /Phone_Screen/
#
# Set the working directory for the container
#
WORKDIR /Phone_Screen/
