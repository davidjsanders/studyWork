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
# Install additional apps for this context here. Remember to do apt-get update
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
# There must ALWAYS be Control.py, v1_00_Control.py
#
COPY Context/Control.py /Context/Context/
COPY Context/v1_00_Control.py /Context/Context/
#
# There must ALWAYS be Context_Database.py, v1_00_Context_Database.py
#
COPY Context/Context_Database.py /Context/Context/
COPY Context/v1_00_Context_Database.py /Context/Context/
#
# Optional Controls
#
COPY Context/Sample_Control.py /Context/Context/
COPY Context/v1_00_Sample_Control.py /Context/Context/
#
COPY Context/Activity_Control.py /Context/Context/
COPY Context/v1_00_Activity_Control.py /Context/Context/
#
#
# Boundary
# --------
#
COPY Context_Boundary/main.py /Context/Context_Boundary/
COPY Context_Boundary/Sample_Boundary.py /Context/Context_Boundary/
COPY Context_Boundary/Activity_Boundary.py /Context/Context_Boundary/
#
# Config Boundary
#
COPY Context_Config_Boundary/Config_Sample_Boundary.py /Context/Context_Config_Boundary/
COPY Context_Config_Boundary/main.py /Context/Context_Config_Boundary/
#
# Config Control
#
COPY Context_Config_Control/Config_Sample_Control.py /Context/Context_Config_Control/
COPY Context_Config_Control/v1_00_Config_Sample_Control.py /Context/Context_Config_Control/
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

