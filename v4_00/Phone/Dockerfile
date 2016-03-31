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
# Set the base image to the correct version, e.g. v1_00 | v2_00 | etc.
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
RUN mkdir /Phone
RUN mkdir /Phone/Phone
RUN mkdir /Phone/Phone_Boundary
RUN mkdir /Phone/Phone_Config_Boundary
RUN mkdir /Phone/Phone_Config_Control
RUN mkdir /Phone/datavolume
#
#
# COPY FILES
# ==========
#
# Copy root files
#
COPY runserver.py /Phone/
COPY startup.sh /Phone/
COPY Phone/main.py /Phone/Phone/
COPY Phone/__init__.py /Phone/Phone/
#
#
# CONTROL
# -------
#
# There must ALWAYS be Control.py, v1_00_Control.py
#
COPY Phone/Control.py /Phone/Phone/
COPY Phone/v1_00_Control.py /Phone/Phone/
#
# There must ALWAYS be Phone_Database.py, v1_00_Phone_Database.py
#
COPY Phone/Phone_Database.py /Phone/Phone/
COPY Phone/v1_00_Phone_Database.py /Phone/Phone/
#
# Optional Controls
#
COPY Phone/Sample_Control.py /Phone/Phone/
COPY Phone/v1_00_Sample_Control.py /Phone/Phone/
#
#
# Boundary
# --------
#
COPY Phone_Boundary/main.py /Phone/Phone_Boundary/
COPY Phone_Boundary/Sample_Boundary.py /Phone/Phone_Boundary/
#
# Config Boundary
#
COPY Phone_Config_Boundary/main.py /Phone/Phone_Config_Boundary/
COPY Phone_Config_Boundary/Config_Sample_Boundary.py /Phone/Phone_Config_Boundary/
COPY Phone_Config_Boundary/Config_Logger_Boundary.py /Phone/Phone_Config_Boundary/
#
# Config Control
#
COPY Phone_Config_Control/Config_Sample_Control.py /Phone/Phone_Config_Control/
COPY Phone_Config_Control/v1_00_Config_Sample_Control.py /Phone/Phone_Config_Control/
COPY Phone_Config_Control/Config_Logger_Control.py /Phone/Phone_Config_Control/
COPY Phone_Config_Control/v1_00_Config_Logger_Control.py /Phone/Phone_Config_Control/
#
#
# Set the working directory for the container
#
WORKDIR /Phone/
# Set the entrypoint
ENTRYPOINT ["/bin/bash"]
# Set default parameters
CMD ["/Phone/startup.sh"]
#
# Create the symbolic link to the base library
#
RUN ln -s /base_lib /Phone/base_lib

