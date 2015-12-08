#
# Dockerfile
# ----------
# Purpose - build the Docker container image for the notification device
#           (bluetooth) to enable the application to run on any platform that
#           supports Docker.
# MAINTAINER David Sanders <dsanders_can@outlook.com>
# Created - 04 Nov 2015
# Last Up - 27 Nov 2015
#
#
# Use the base Python image which includes Python3, Flask, Flask_Restful, and
# 
FROM dsanderscan/pythonbase
#
# Create the /bluetooth directory
RUN mkdir /bluetooth
RUN mkdir /bluetooth/schemas
#RUN mkdir /bluetooth/datavol
#
# Create the /bluetooth python directory structure
#RUN mkdir /bluetooth/bluetooth
#RUN mkdir /bluetooth/bluetooth/static
#RUN mkdir /bluetooth/bluetooth/templates
#RUN mkdir /bluetooth/bluetooth/resources
#
# copy the files required for the application
#
COPY startup.sh /bluetooth/
COPY runserver.py /bluetooth/
COPY bluetooth_uwsgi.ini /bluetooth/
#COPY bluetooth_uwsgi.conf /bluetooth/
COPY bluetooth/__init__.py /bluetooth/bluetooth/
COPY bluetooth/ /bluetooth/
COPY bluetooth/main.py /bluetooth/bluetooth/
COPY bluetooth/resources/Config.py /bluetooth/bluetooth/resources/
COPY bluetooth/resources/Response.py /bluetooth/bluetooth/resources/
COPY schemas/ /bluetooth/schemas/
#COPY schemas/links.json /bluetooth/schemas/
#COPY schemas/notification.json /bluetooth/schemas/
#COPY datavol/bluetooth.db /bluetooth/datavol/bluetooth.db
#
# Set the working directory for the container
#
WORKDIR /bluetooth/
