#
# Dockerfile
# ----------
# Purpose - build the Docker container image for the notification device
#           (notifications) to enable the application to run on any platform that
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
# Create the /notifications directory
RUN mkdir /notifications
RUN mkdir /notifications/schemas
#RUN mkdir /notifications/datavol
#
# Create the /notifications python directory structure
#RUN mkdir /notifications/notifications
#RUN mkdir /notifications/notifications/static
#RUN mkdir /notifications/notifications/templates
#RUN mkdir /notifications/notifications/resources
#
# copy the files required for the application
#
COPY startup.sh /notifications/
COPY runserver.py /notifications/
COPY notifications_uwsgi.ini /notifications/
COPY notifications_uwsgi.conf /notifications/
COPY notifications/__init__.py /notifications/notifications/
COPY notifications/ /notifications/
COPY notifications/main.py /notifications/notifications/
COPY notifications/resources/Notification_Boundary.py /notifications/notifications/resources/
COPY notifications/resources/Notification_DB.py /notifications/notifications/resources/
COPY notifications/resources/Notification.py /notifications/notifications/resources/
COPY notifications/resources/Notification_Schema.py /notifications/notifications/resources/
COPY notifications/resources/Notification_Pair.py /notifications/notifications/resources/
COPY notifications/resources/Notification_Pair_Schema.py /notifications/notifications/resources/
COPY notifications/resources/Response.py /notifications/notifications/resources/
COPY notifications/resources/Config.py /notifications/notifications/resources/
COPY schemas/ /notifications/schemas/
COPY schemas/links.json /notifications/schemas/
COPY schemas/notification.json /notifications/schemas/
COPY datavol/notifications.db /notifications/datavol/notifications.db
#
# Set the working directory for the container
#
WORKDIR /notifications/
