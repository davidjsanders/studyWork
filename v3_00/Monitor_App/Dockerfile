#
# Dockerfile
# ----------
# Purpose - build the Docker container image for the Monitor_App device
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
# 07 Jan 2016  | D Sanders      | Add config control & centralized logging
#
#
# Use the base Python image which includes Python3, Flask, Flask_Restful, and
# 
FROM dsanderscan/mscit_base
#
# Install additional apps for this module
#
# Install Redis
#
#RUN apt-get update
#RUN apt-get install -y redis-server
#
# Install the python Redis module
#
#RUN pip3 install redis
#
# Create the directory structures
##
# Create the directory structures
RUN mkdir /Monitor_App
RUN mkdir /Monitor_App/Monitor_App
RUN mkdir /Monitor_App/Monitor_App_Boundary
RUN mkdir /Monitor_App/Monitor_App_Config_Boundary
RUN mkdir /Monitor_App/Monitor_App_Config_Control
RUN mkdir /Monitor_App/datavolume
#
# copy the files required for the application
#
COPY runserver.py /Monitor_App/
COPY startup.sh /Monitor_App/
COPY Monitor_App/__init__.py /Monitor_App/Monitor_App/
COPY Monitor_App/main.py /Monitor_App/Monitor_App/
#
COPY Monitor_App/Control.py /Monitor_App/Monitor_App/
COPY Monitor_App/v3_00_Control.py /Monitor_App/Monitor_App/
#
COPY Monitor_App/App_Control.py /Monitor_App/Monitor_App/
COPY Monitor_App/v3_00_App_Control.py /Monitor_App/Monitor_App/
#
COPY Monitor_App/App_Launched_Control.py /Monitor_App/Monitor_App/
COPY Monitor_App/v3_00_App_Launched_Control.py /Monitor_App/Monitor_App/
#
COPY Monitor_App/Location_Processor.py /Monitor_App/Monitor_App/
COPY Monitor_App/v3_00_Location_Processor.py /Monitor_App/Monitor_App/
#
COPY Monitor_App/Monitor_App_Database.py /Monitor_App/Monitor_App/
COPY Monitor_App/v3_00_Monitor_App_Database.py /Monitor_App/Monitor_App/
#
COPY Monitor_App/State_Control.py /Monitor_App/Monitor_App/
COPY Monitor_App/v3_00_State_Control.py /Monitor_App/Monitor_App/
#
COPY Monitor_App_Boundary/__init__.py /Monitor_App/Monitor_App_Boundary/
COPY Monitor_App_Boundary/main.py /Monitor_App/Monitor_App_Boundary/
COPY Monitor_App_Boundary/State_Boundary.py /Monitor_App/Monitor_App_Boundary/
COPY Monitor_App_Boundary/App_Launched_Boundary.py /Monitor_App/Monitor_App_Boundary/
COPY Monitor_App_Boundary/App_Boundary.py /Monitor_App/Monitor_App_Boundary/
#
COPY Monitor_App_Config_Boundary/Config_Logger_Boundary.py \
    /Monitor_App/Monitor_App_Config_Boundary/
COPY Monitor_App_Config_Boundary/v3_00_Config_Logger_Boundary.py \
    /Monitor_App/Monitor_App_Config_Boundary/
#
COPY Monitor_App_Config_Boundary/main.py \
    /Monitor_App/Monitor_App_Config_Boundary/
#
COPY Monitor_App_Config_Control/Config_Logger_Control.py \
    /Monitor_App/Monitor_App_Config_Control/
COPY Monitor_App_Config_Control/v3_00_Config_Logger_Control.py \
    /Monitor_App/Monitor_App_Config_Control/
#
# Set the working directory for the container
#
WORKDIR /Monitor_App/
# Set the entrypoint
ENTRYPOINT ["/bin/bash"]
# Set default parameters
CMD ["/Monitor_App/startup.sh"]
#
# Create the symbolic link to the base library
#
RUN ln -s /base_lib /Monitor_App/base_lib

