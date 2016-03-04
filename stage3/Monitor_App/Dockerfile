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
# 04 Mar 2016  | D Sanders      | First stage 3 version.
#
#
# Use the base monitor_app
# 
FROM dsanderscan/mscit_stage2_monitor_app
#
# copy the files required for the application
#
COPY Monitor_App/App_Launched_Control.py /Monitor_App/Monitor_App/
COPY Monitor_App/Control.py /Monitor_App/Monitor_App/
COPY Monitor_App/Location_Processor.py /Monitor_App/Monitor_App/
COPY Monitor_App/Monitor_App_Database.py /Monitor_App/Monitor_App/
COPY Monitor_App_Config_Boundary/Config_Message_Boundary.py \
    /Monitor_App/Monitor_App_Config_Boundary/
COPY Monitor_App_Config_Boundary/main.py \
    /Monitor_App/Monitor_App_Config_Boundary/
COPY Monitor_App_Config_Control/Config_Message_Control.py \
    /Monitor_App/Monitor_App_Config_Control/
#
WORKDIR /Monitor_App/
ENTRYPOINT ["/bin/bash"] # Set the entrypoint
CMD ["/Monitor_App/startup.sh"]                                # Set default parameters
