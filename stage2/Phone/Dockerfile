#
# Dockerfile
# ----------
# Purpose - build the Docker container image for the Phone device
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
RUN mkdir /Phone
RUN mkdir /Phone/Phone
RUN mkdir /Phone/Phone_Boundary
#
# copy the files required for the application
#
COPY runserver.py /Phone/
COPY startup.sh /Phone/
COPY Phone/__init__.py /Phone/Phone/
COPY Phone/main.py /Phone/Phone/
COPY Phone/Control.py /Phone/Phone/
COPY Phone/Location_Control.py /Phone/Phone/
COPY Phone/Lock_Control.py /Phone/Phone/
COPY Phone/Notification_Control.py /Phone/Phone/
COPY Phone/Phone_Database.py /Phone/Phone/
COPY Phone_Boundary/__init__.py /Phone/Phone_Boundary/
COPY Phone_Boundary/main.py /Phone/Phone_Boundary/
COPY Phone_Boundary/Location_Boundary.py /Phone/Phone_Boundary/
COPY Phone_Boundary/Lock_Boundary.py /Phone/Phone_Boundary/
COPY Phone_Boundary/Notification_Boundary.py /Phone/Phone_Boundary/
COPY Phone_Boundary/Unlock_Boundary.py /Phone/Phone_Boundary/
COPY Phone_Boundary/Versions_Boundary.py /Phone/Phone_Boundary/
#
# Set the working directory for the container
#
WORKDIR /Phone/
