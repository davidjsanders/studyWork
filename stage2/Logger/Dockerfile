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
# Create the directory structures
RUN mkdir /Logger
RUN mkdir /Logger/Logger
RUN mkdir /Logger/Logger_Boundary
RUN mkdir /Logger/Logger_Config_Boundary
RUN mkdir /Logger/Logger_Config_Control
#
# copy the files required for the application
#
COPY runserver.py /Logger/
COPY startup.sh /Logger/
COPY Logger/__init__.py /Logger/Logger/
COPY Logger/main.py /Logger/Logger/
COPY Logger/Control.py /Logger/Logger/
COPY Logger/Check_Control.py /Logger/Logger/
COPY Logger/Logger_Database.py /Logger/Logger/
COPY Logger_Boundary/__init__.py /Logger/Logger_Boundary/
COPY Logger_Boundary/main.py /Logger/Logger_Boundary/
COPY Logger_Boundary/Check_Boundary.py /Logger/Logger_Boundary/
COPY Logger_Config_Boundary/Config_Hotspot_Boundary.py /Logger/Logger_Config_Boundary/
COPY Logger_Config_Boundary/main.py /Logger/Logger_Config_Boundary/
COPY Logger_Config_Control/Config_Hotspot_Control.py /Logger/Logger_Config_Control/
#
# Set the working directory for the container
#
WORKDIR /Logger/
