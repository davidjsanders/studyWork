#
# Dockerfile
# ----------
# Purpose - build the Docker container image for the Module device
#           to enable the application to run on any platform that
#           supports Docker.
#
# MAINTAINER David Sanders <dsanders_can@outlook.com>
#
# Revision History
# -----------------------------------------------------------------------------
# Date         | By             | Reason
# -----------------------------------------------------------------------------
# 28 Mar 2016  | D Sanders      | First version of template.
#
#
# BASE IMAGE - IMPORTANT
# ======================
#
# Set the base image to the correct version, e.g. v4_00 | v2_00 | etc.
#
FROM dsanderscan/mscit_base
#
#
# ADDITIONAL APPS
# ===============
# Install additional apps for this module here. Remember to do apt-get update
# if needed.
#
#
# CREATE DIRECTORY STRUCTURES
# ===========================
RUN mkdir /Context
RUN mkdir /Context/Context
RUN mkdir /Context/Context_Boundary
RUN mkdir /Context/Context_Config_Boundary
RUN mkdir /Context/Context_Config_Control
RUN mkdir /Context/datavolume
#
#
# COPY FILES
# ==========
#
# Copy root files
#
COPY runserver.py /Context/
COPY startup.sh /Context/
COPY Context/main.py /Context/Context/
COPY Context/__init__.py /Context/Context/
#
#
# CONTROL
# -------
#
# There must ALWAYS be Control.py, v4_00_Control.py
#
COPY Context/Control.py /Context/Context/
COPY Context/v4_00_Control.py /Context/Context/
#
# There must ALWAYS be Context_Database.py, v4_00_Context_Database.py
#
COPY Context/Context_Database.py /Context/Context/
COPY Context/v4_00_Context_Database.py /Context/Context/
#
# Optional Controls
#
COPY Context/Sample_Control.py /Context/Context/
COPY Context/v4_00_Sample_Control.py /Context/Context/
#
#
# Boundary
# --------
#
COPY Context_Boundary/main.py /Context/Context_Boundary/
COPY Context_Boundary/Sample_Boundary.py /Context/Context_Boundary/
#
# Config Boundary
#
COPY Context_Config_Boundary/main.py /Context/Context_Config_Boundary/
COPY Context_Config_Boundary/Config_Context_Boundary.py /Context/Context_Config_Boundary/
COPY Context_Config_Boundary/Config_Sample_Boundary.py /Context/Context_Config_Boundary/
COPY Context_Config_Boundary/Config_Logger_Boundary.py /Context/Context_Config_Boundary/
#
# Config Control
#
COPY Context_Config_Control/Config_Context_Control.py /Context/Context_Config_Control/
COPY Context_Config_Control/v4_00_Config_Context_Control.py /Context/Context_Config_Control/
COPY Context_Config_Control/Config_Sample_Control.py /Context/Context_Config_Control/
COPY Context_Config_Control/v4_00_Config_Sample_Control.py /Context/Context_Config_Control/
COPY Context_Config_Control/Config_Logger_Control.py /Context/Context_Config_Control/
COPY Context_Config_Control/v4_00_Config_Logger_Control.py /Context/Context_Config_Control/
#
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


### Generated Boundary for service: State
COPY Context_Boundary/State_Boundary.py /Context/Context_Boundary/

### Generated Control for service: State
COPY Context/State_Control.py /Context/Context/

### Generated Control for service: v4_00_State
COPY Context/v4_00_State_Control.py /Context/Context/

### Generated Boundary for service: Query
COPY Context_Boundary/Query_Boundary.py /Context/Context_Boundary/

### Generated Control for service: Query
COPY Context/Query_Control.py /Context/Context/

### Generated Control for service: v4_00_Query
COPY Context/v4_00_Query_Control.py /Context/Context/

### Generated Boundary for service: Notify
COPY Context_Boundary/Notify_Boundary.py /Context/Context_Boundary/

### Generated Control for service: Notify
COPY Context/Notify_Control.py /Context/Context/

### Generated Control for service: v4_00_Notify
COPY Context/v4_00_Notify_Control.py /Context/Context/

### Generated Boundary for service: Subscribe
COPY Context_Boundary/Subscribe_Boundary.py /Context/Context_Boundary/

### Generated Control for service: Subscribe
COPY Context/Subscribe_Control.py /Context/Context/

### Generated Control for service: v4_00_Subscribe
COPY Context/v4_00_Subscribe_Control.py /Context/Context/

### Generated Config Boundary for service: Preferences
COPY Context_Config_Boundary/Preferences_Boundary.py /Context/Context_Config_Boundary/

### Generated Config Control for service: Preferences
COPY Context_Config_Control/Config_Preferences_Control.py /Context/Context_Config_Control/

### Generated Config Control for service: v4_00_Preferences
COPY Context_Config_Control/v4_00_Config_Preferences_Control.py /Context/Context_Config_Control/
