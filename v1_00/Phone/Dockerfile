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
# 24 Jan 2016  | D Sanders      | First version.
# 31 Jan 2016  | D Sanders      | Update to include config boundary & controls
# 07 Jan 2016  | D Sanders      | Add centralized logging
#
# Use the base Python image which includes Python3, Flask, and Flask_Restful
# 
FROM dsanderscan/mscit_stage2_base
#
# Install additional apps for this module
#
# Install Redis
#
RUN apt-get update
RUN apt-get install -y --fix-missing redis-server
#
# Install the python Redis module
#
RUN pip3 install redis
#
# Create the directory structures
#
RUN mkdir /Phone
RUN mkdir /Phone/Phone
RUN mkdir /Phone/Phone_Boundary
RUN mkdir /Phone/Phone_Config_Boundary
RUN mkdir /Phone/Phone_Config_Control
RUN mkdir /Phone/datavolume
#
# copy the files required for the application
#
COPY runserver.py /Phone/
COPY startup.sh /Phone/
COPY Phone/Control.py /Phone/Phone/
COPY Phone/__init__.py /Phone/Phone/
COPY Phone/Location_Control.py /Phone/Phone/
COPY Phone/main.py /Phone/Phone/
COPY Phone/Notification_Control.py /Phone/Phone/
COPY Phone/Phone_Database.py /Phone/Phone/
#
# Boundary
#
COPY Phone_Boundary/main.py /Phone/Phone_Boundary/
COPY Phone_Boundary/Location_Boundary.py /Phone/Phone_Boundary/
COPY Phone_Boundary/Notification_Boundary.py /Phone/Phone_Boundary/
#
# Config Boundary
#
COPY Phone_Config_Boundary/Config_Help_Boundary.py /Phone/Phone_Config_Boundary/
COPY Phone_Config_Boundary/Config_Launch_Boundary.py /Phone/Phone_Config_Boundary/
COPY Phone_Config_Boundary/Config_Location_Boundary.py /Phone/Phone_Config_Boundary/
COPY Phone_Config_Boundary/Config_Lock_Boundary.py /Phone/Phone_Config_Boundary/
COPY Phone_Config_Boundary/Config_Logger_Boundary.py /Phone/Phone_Config_Boundary/
COPY Phone_Config_Boundary/Config_Monitor_App_Boundary.py /Phone/Phone_Config_Boundary/
COPY Phone_Config_Boundary/Config_Pair_Boundary.py /Phone/Phone_Config_Boundary/
COPY Phone_Config_Boundary/Config_Push_Notifications_Boundary.py /Phone/Phone_Config_Boundary/
COPY Phone_Config_Boundary/Config_Unlock_Boundary.py /Phone/Phone_Config_Boundary/
COPY Phone_Config_Boundary/main.py /Phone/Phone_Config_Boundary/
#
# Config Control
#
COPY Phone_Config_Control/Config_Help_Control.py /Phone/Phone_Config_Control/
COPY Phone_Config_Control/Config_Launch_Control.py /Phone/Phone_Config_Control/
COPY Phone_Config_Control/Config_Location_Control.py /Phone/Phone_Config_Control/
COPY Phone_Config_Control/Config_Lock_Control.py /Phone/Phone_Config_Control/
COPY Phone_Config_Control/Config_Logger_Control.py /Phone/Phone_Config_Control/
COPY Phone_Config_Control/Config_Monitor_App_Control.py /Phone/Phone_Config_Control/
COPY Phone_Config_Control/Config_Pair_Control.py /Phone/Phone_Config_Control/
COPY Phone_Config_Control/Config_Push_Notifications_Control.py /Phone/Phone_Config_Control/
#
# Set the working directory for the container
#
WORKDIR /Phone/
# Set the entrypoint
ENTRYPOINT ["/bin/bash"]
# Set default parameters
CMD ["/Phone/startup.sh"]
