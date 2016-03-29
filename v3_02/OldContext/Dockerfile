#
# Dockerfile
# ----------
# Purpose - build the Docker container image for the Context device
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
FROM dsanderscan/mscit_v3_00_base
#
# Install additional apps for this module
#
# Create the directory structures
#
RUN mkdir /Context
RUN mkdir /Context/Context
RUN mkdir /Context/Context_Boundary
RUN mkdir /Context/Context_Config_Boundary
RUN mkdir /Context/Context_Config_Control
RUN mkdir /Context/datavolume
#
# copy the files required for the application
#
COPY runserver.py /Context/
COPY startup.sh /Context/
COPY Context/main.py /Context/Context/
COPY Context/__init__.py /Context/Context/
#
COPY Context/Control.py /Context/Context/
COPY Context/v3_00_Control.py /Context/Context/
#
COPY Context/Location_Control.py /Context/Context/
COPY Context/v3_00_Location_Control.py /Context/Context/
#
COPY Context/Notification_Control.py /Context/Context/
COPY Context/v3_00_Notification_Control.py /Context/Context/
#
COPY Context/Context_Database.py /Context/Context/
COPY Context/v3_00_Context_Database.py /Context/Context/
#
# Boundary
#
COPY Context_Boundary/main.py /Context/Context_Boundary/
COPY Context_Boundary/Location_Boundary.py /Context/Context_Boundary/
COPY Context_Boundary/Notification_Boundary.py /Context/Context_Boundary/
#
# Config Boundary
#
COPY Context_Config_Boundary/Config_Launch_Boundary.py /Context/Context_Config_Boundary/
COPY Context_Config_Boundary/Config_Location_Boundary.py /Context/Context_Config_Boundary/
COPY Context_Config_Boundary/Config_Lock_Boundary.py /Context/Context_Config_Boundary/
COPY Context_Config_Boundary/Config_Logger_Boundary.py /Context/Context_Config_Boundary/
COPY Context_Config_Boundary/Config_Monitor_App_Boundary.py /Context/Context_Config_Boundary/
COPY Context_Config_Boundary/Config_Pair_Boundary.py /Context/Context_Config_Boundary/
COPY Context_Config_Boundary/Config_Push_Notifications_Boundary.py /Context/Context_Config_Boundary/
COPY Context_Config_Boundary/Config_Screen_Boundary.py /Context/Context_Config_Boundary/
COPY Context_Config_Boundary/Config_Unlock_Boundary.py /Context/Context_Config_Boundary/
COPY Context_Config_Boundary/main.py /Context/Context_Config_Boundary/
#
# Config Control
#
COPY Context_Config_Control/Config_Launch_Control.py /Context/Context_Config_Control/
COPY Context_Config_Control/v3_00_Config_Launch_Control.py /Context/Context_Config_Control/
#
COPY Context_Config_Control/Config_Location_Control.py /Context/Context_Config_Control/
COPY Context_Config_Control/v3_00_Config_Location_Control.py /Context/Context_Config_Control/
#
COPY Context_Config_Control/Config_Lock_Control.py /Context/Context_Config_Control/
COPY Context_Config_Control/v3_00_Config_Lock_Control.py /Context/Context_Config_Control/
#
COPY Context_Config_Control/Config_Logger_Control.py /Context/Context_Config_Control/
COPY Context_Config_Control/v3_00_Config_Logger_Control.py /Context/Context_Config_Control/
#
COPY Context_Config_Control/Config_Monitor_App_Control.py /Context/Context_Config_Control/
COPY Context_Config_Control/v3_00_Config_Monitor_App_Control.py /Context/Context_Config_Control/
#
COPY Context_Config_Control/Config_Pair_Control.py /Context/Context_Config_Control/
COPY Context_Config_Control/v3_00_Config_Pair_Control.py /Context/Context_Config_Control/
#
COPY Context_Config_Control/Config_Push_Notifications_Control.py /Context/Context_Config_Control/
COPY Context_Config_Control/v3_00_Config_Push_Notifications_Control.py /Context/Context_Config_Control/
#
COPY Context_Config_Control/Config_Screen_Control.py /Context/Context_Config_Control/
COPY Context_Config_Control/v3_00_Config_Screen_Control.py /Context/Context_Config_Control/
#
# Set the working directory for the container
#
WORKDIR /Context/
# Set the entrypoint
ENTRYPOINT ["/bin/bash"]
# Set default parameters
CMD ["/Context/startup.sh"]
#
# Create the symbolic link to the base library
#
RUN ln -s /base_lib /Context/base_lib

