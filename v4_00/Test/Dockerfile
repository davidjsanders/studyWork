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
RUN mkdir /Test
RUN mkdir /Test/Test
RUN mkdir /Test/Test_Boundary
RUN mkdir /Test/Test_Config_Boundary
RUN mkdir /Test/Test_Config_Control
RUN mkdir /Test/datavolume
#
#
# COPY FILES
# ==========
#
# Copy root files
#
COPY runserver.py /Test/
COPY startup.sh /Test/
COPY Test/main.py /Test/Test/
COPY Test/__init__.py /Test/Test/
#
#
# CONTROL
# -------
#
# There must ALWAYS be Control.py, v1_00_Control.py
#
COPY Test/Control.py /Test/Test/
COPY Test/v1_00_Control.py /Test/Test/
#
# There must ALWAYS be Test_Database.py, v1_00_Test_Database.py
#
COPY Test/Test_Database.py /Test/Test/
COPY Test/v1_00_Test_Database.py /Test/Test/
#
# Optional Controls
#
COPY Test/Sample_Control.py /Test/Test/
COPY Test/v1_00_Sample_Control.py /Test/Test/
#
#
# Boundary
# --------
#
COPY Test_Boundary/main.py /Test/Test_Boundary/
COPY Test_Boundary/Sample_Boundary.py /Test/Test_Boundary/
#
# Config Boundary
#
COPY Test_Config_Boundary/main.py /Test/Test_Config_Boundary/
COPY Test_Config_Boundary/Config_Sample_Boundary.py /Test/Test_Config_Boundary/
COPY Test_Config_Boundary/Config_Logger_Boundary.py /Test/Test_Config_Boundary/
#
# Config Control
#
COPY Test_Config_Control/Config_Sample_Control.py /Test/Test_Config_Control/
COPY Test_Config_Control/v1_00_Config_Sample_Control.py /Test/Test_Config_Control/
COPY Test_Config_Control/Config_Logger_Control.py /Test/Test_Config_Control/
COPY Test_Config_Control/v1_00_Config_Logger_Control.py /Test/Test_Config_Control/
#
#
# Set the working directory for the container
#
WORKDIR /Test/
# Set the entrypoint
ENTRYPOINT ["/bin/bash"]
# Set default parameters
CMD ["/Test/startup.sh"]
#
# Create the symbolic link to the base library
#
RUN ln -s /base_lib /Test/base_lib

