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
FROM dsanderscan/mscit_v3_00_base
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
RUN mkdir /Module
RUN mkdir /Module/Module
RUN mkdir /Module/Module_Boundary
RUN mkdir /Module/Module_Config_Boundary
RUN mkdir /Module/Module_Config_Control
RUN mkdir /Module/datavolume
#
#
# COPY FILES
# ==========
#
# Copy root files
#
COPY runserver.py /Module/
COPY startup.sh /Module/
COPY Module/main.py /Module/Module/
COPY Module/__init__.py /Module/Module/
#
#
# CONTROL
# -------
#
# There must ALWAYS be Control.py, v1_00_Control.py
#
COPY Module/Control.py /Module/Module/
COPY Module/v1_00_Control.py /Module/Module/
#
# There must ALWAYS be Module_Database.py, v1_00_Module_Database.py
#
COPY Module/Module_Database.py /Module/Module/
COPY Module/v1_00_Module_Database.py /Module/Module/
#
# Optional Controls
#
COPY Module/Sample_Control.py /Module/Module/
COPY Module/v1_00_Sample_Control.py /Module/Module/
#
#
# Boundary
# --------
#
COPY Module_Boundary/main.py /Module/Module_Boundary/
COPY Module_Boundary/Sample_Boundary.py /Module/Module_Boundary/
#
# Config Boundary
#
COPY Module_Config_Boundary/Config_Sample_Boundary.py /Module/Module_Config_Boundary/
COPY Module_Config_Boundary/main.py /Module/Module_Config_Boundary/
#
# Config Control
#
COPY Module_Config_Control/Config_Sample_Control.py /Module/Module_Config_Control/
COPY Module_Config_Control/v1_00_Config_Sample_Control.py /Module/Module_Config_Control/
#
#
# Set the working directory for the container
#
WORKDIR /Module/
# Set the entrypoint
ENTRYPOINT ["/bin/bash"]
# Set default parameters
CMD ["/Module/startup.sh"]
#
# Create the symbolic link to the base library
#
RUN ln -s /base_lib /Module/base_lib

