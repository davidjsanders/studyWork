#
# Dockerfile
# ----------
# Purpose - build the Docker container image for the notification device
#           (notes) to enable the application to run on any platform that
#           supports Docker.
# MAINTAINER David Sanders <dsanders_can@outlook.com>
# Created - 04 Nov 2015
# Last Up - 04 Nov 2015
#
#
# Use the base Python image which includes Python3, Flask, Flask_Restful, and
# 
FROM dsanders/pythonbase
#
# Create the /notes directory
RUN mkdir /notes
#
# Create the /notes python directory structure
RUN mkdir /notes/notes
RUN mkdir /notes/notes/static
RUN mkdir /notes/notes/templates
RUN mkdir /notes/notes/resources
#
# copy the files required for the application
#
COPY startup.sh /notes/
COPY runserver.py /notes/
COPY notes_final.ini /notes/
COPY notes/__init__.py /notes/notes/
COPY notes/main.py /notes/notes/
COPY notes/resources/Config.py /notes/notes/resources/
COPY notes/resources/Notifications.py /notes/notes/resources/
COPY notes/resources/Lock.py /notes/notes/resources/
COPY notes/resources/Persist.py /notes/notes/resources/
COPY notes/resources/Helper.py /notes/notes/resources/
#
# Set the working directory for the container
#
WORKDIR /notes/
#
# Update nginx configuration
#
RUN rm -r -f /etc/nginx/sites-enabled/default
RUN ln -s /notes/notes_final.conf /etc/nginx/conf.d/notes_final.conf
