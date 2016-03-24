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
RUN mkdir /Logger
RUN mkdir /Logger/Logger
RUN mkdir /Logger/Logger_Boundary
RUN mkdir /Logger/datavolume
#
# copy the files required for the application
#
COPY runserver.py /Logger/
COPY startup.sh /Logger/
COPY Logger/__init__.py /Logger/Logger/
COPY Logger/main.py /Logger/Logger/
#
# Control
#
COPY Logger/Control.py /Logger/Logger/
COPY Logger/v3_00_Control.py /Logger/Logger/
#
COPY Logger/Log_Control.py /Logger/Logger/
COPY Logger/v3_00_Log_Control.py /Logger/Logger/
#
COPY Logger/Logger_Database.py /Logger/Logger/
COPY Logger/v3_00_Logger_Database.py /Logger/Logger/
#
COPY Logger/Logging_Processor.py /Logger/Logger
COPY Logger/v3_00_Logging_Processor.py /Logger/Logger
#
# Boundary
#
COPY Logger_Boundary/__init__.py /Logger/Logger_Boundary/
COPY Logger_Boundary/main.py /Logger/Logger_Boundary/
COPY Logger_Boundary/Log_Boundary.py /Logger/Logger_Boundary/
#
# Set the working directory for the container
#
WORKDIR /Logger/
# Set the entrypoint
ENTRYPOINT ["/bin/bash"]
# Set default parameters
CMD ["/Logger/startup.sh"]
#
# Create the symbolic link to the base library
#
RUN ln -s /base_lib /Logger/base_lib

