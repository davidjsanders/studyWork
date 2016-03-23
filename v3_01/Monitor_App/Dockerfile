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
# 18 Mar 2016  | D Sanders      | First version, based on v3_00.
#
#
# Use the base Python image which includes Python3, Flask, Flask_Restful, and
# 
FROM dsanderscan/mscit_v3_00_monitor_app
#
# Copy v3_01 apps
#
COPY Monitor_App/Control.py /Monitor_App/Monitor_App/
COPY Monitor_App/v3_01_Control.py /Monitor_App/Monitor_App/
#
COPY Monitor_App/App_Launched_Control.py /Monitor_App/Monitor_App/
COPY Monitor_App/Location_Processor.py /Monitor_App/Monitor_App/
COPY Monitor_App_Config_Boundary/main.py /Monitor_App/Monitor_App_Config_Boundary/
COPY Monitor_App_Config_Boundary/Config_Message_Boundary.py \
  /Monitor_App/Monitor_App_Config_Boundary/
COPY Monitor_App_Config_Control/Config_Message_Control.py \
  /Monitor_App/Monitor_App_Config_Control/

