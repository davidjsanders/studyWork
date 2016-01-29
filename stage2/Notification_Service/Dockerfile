#
# Dockerfile
# ----------
# Purpose - build the Docker container image for the Notification_Service device
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
RUN mkdir /Notification_Service
RUN mkdir /Notification_Service/Notification_Service
RUN mkdir /Notification_Service/Notification_Service_Boundary
#
# copy the files required for the application
#
COPY runserver.py /Notification_Service/
COPY startup.sh /Notification_Service/
COPY Notification_Service/__init__.py \
   /Notification_Service/Notification_Service/
COPY Notification_Service/main.py \
   /Notification_Service/Notification_Service/
COPY Notification_Service/Control.py /Notification_Service/Notification_Service/
COPY Notification_Service/Location_Control.py /Notification_Service/Notification_Service/
COPY Notification_Service/Lock_Control.py /Notification_Service/Notification_Service/
COPY Notification_Service/Notification_Control.py /Notification_Service/Notification_Service/
COPY Notification_Service/Notification_Service_Database.py /Notification_Service/Notification_Service/
COPY Notification_Service_Boundary/__init__.py /Notification_Service/Notification_Service_Boundary/
COPY Notification_Service_Boundary/main.py /Notification_Service/Notification_Service_Boundary/
COPY Notification_Service_Boundary/Location_Boundary.py /Notification_Service/Notification_Service_Boundary/
COPY Notification_Service_Boundary/Lock_Boundary.py /Notification_Service/Notification_Service_Boundary/
COPY Notification_Service_Boundary/Notification_Boundary.py /Notification_Service/Notification_Service_Boundary/
COPY Notification_Service_Boundary/Unlock_Boundary.py /Notification_Service/Notification_Service_Boundary/
COPY Notification_Service_Boundary/Versions_Boundary.py /Notification_Service/Notification_Service_Boundary/
#
# Set the working directory for the container
#
WORKDIR /Notification_Service/
