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
# 24 Jan 2016  | D Sanders      | First version.
# 05 Feb 2016  | D Sanders      | Update logging, multi-use, superclass & docker
# 10 Feb 2016  | D Sanders      | Update logging to central logger
#
# Use the base Python image which includes Python3, Flask, Flask_Restful, and
# 
FROM dsanderscan/mscit_stage2_base
#
# Create the directory structures
RUN mkdir /Notification_Service
RUN mkdir /Notification_Service/Notification_Service
RUN mkdir /Notification_Service/Notification_Service_Boundary
RUN mkdir /Notification_Service/Notification_Service_Config_Boundary
RUN mkdir /Notification_Service/Notification_Service_Config_Control
RUN mkdir /Notification_Service/datavolume
#
# Install additional apps for this module
#
# Install Redis
#
RUN apt-get install -y redis-server
#
# Install the python Redis module
#
RUN pip3 install redis
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
COPY Notification_Service/Notification_Processor.py /Notification_Service/Notification_Service/
COPY Notification_Service/Notification_Receiver.py /Notification_Service/Notification_Service/
COPY Notification_Service/Notification_Service_Database.py /Notification_Service/Notification_Service/
COPY Notification_Service/Notification_Push_Control.py /Notification_Service/Notification_Service/
COPY Notification_Service_Boundary/main.py /Notification_Service/Notification_Service_Boundary/
COPY Notification_Service_Boundary/Notification_Receive_Boundary.py \
    /Notification_Service/Notification_Service_Boundary/
COPY Notification_Service_Boundary/Notification_Push_Boundary.py \
    /Notification_Service/Notification_Service_Boundary/
COPY Notification_Service_Config_Boundary/main.py \
    /Notification_Service/Notification_Service_Config_Boundary/
COPY Notification_Service_Config_Boundary/Config_Logger_Boundary.py \
    /Notification_Service/Notification_Service_Config_Boundary/
COPY Notification_Service_Config_Control/Config_Logger_Control.py \
    /Notification_Service/Notification_Service_Config_Control/
#
# Set the working directory for the container
#
WORKDIR /Notification_Service/
# Set the entrypoint
ENTRYPOINT ["/bin/bash"]
# Set default parameters
CMD ["/Notification_Service/startup.sh"]
