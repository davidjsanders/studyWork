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
FROM dsanderscan/mscit_v3_00_base
#
# Create the directory structures
RUN mkdir /Location_Service
RUN mkdir /Location_Service/Location_Service
RUN mkdir /Location_Service/Location_Service_Boundary
RUN mkdir /Location_Service/Location_Service_Config_Boundary
RUN mkdir /Location_Service/Location_Service_Config_Control
RUN mkdir /Location_Service/datavolume
#
# copy the files required for the application
#
COPY runserver.py /Location_Service/
COPY startup.sh /Location_Service/
COPY Location_Service/__init__.py /Location_Service/Location_Service/
COPY Location_Service/main.py /Location_Service/Location_Service/
COPY Location_Service/Control.py /Location_Service/Location_Service/
COPY Location_Service/Check_Control.py /Location_Service/Location_Service/
COPY Location_Service/Location_Service_Database.py \
    /Location_Service/Location_Service/
COPY Location_Service_Boundary/__init__.py \
    /Location_Service/Location_Service_Boundary/
COPY Location_Service_Boundary/main.py \
    /Location_Service/Location_Service_Boundary/
COPY Location_Service_Boundary/Check_Boundary.py \
    /Location_Service/Location_Service_Boundary/
COPY Location_Service_Config_Boundary/Config_Hotspot_Boundary.py \
    /Location_Service/Location_Service_Config_Boundary/
COPY Location_Service_Config_Boundary/Config_Logger_Boundary.py \
    /Location_Service/Location_Service_Config_Boundary/
COPY Location_Service_Config_Boundary/main.py \
    /Location_Service/Location_Service_Config_Boundary/
COPY Location_Service_Config_Control/Config_Hotspot_Control.py \
    /Location_Service/Location_Service_Config_Control/
COPY Location_Service_Config_Control/Config_Logger_Control.py \
    /Location_Service/Location_Service_Config_Control/
#
# Set the working directory for the container
#
WORKDIR /Location_Service/
# Set the entrypoint
ENTRYPOINT ["/bin/bash"]
# Set default parameters
CMD ["/Location_Service/startup.sh"]
#
# Create the symbolic link to the base library
#
RUN ln -s /base_lib /Location_Service/base_lib

