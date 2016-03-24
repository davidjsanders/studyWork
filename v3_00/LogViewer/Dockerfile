#
# Dockerfile
# ----------
# Purpose - build the Docker container image for the log viewer
#           to enable the application to run on any platform that
#           supports Docker.
#
# MAINTAINER David Sanders <dsanders_can@outlook.com>
#
# Revision History
# -----------------------------------------------------------------------------
# Date         | By             | Reason
# -----------------------------------------------------------------------------
# 20 Feb 2016  | D Sanders      | First version.
#

# Base Debian Linux image
FROM debian

# Update core packages
RUN apt-get update

# Install python & clean packages
RUN apt-get install -y \
    python3 \
    python3-pip \
&& rm -rf /var/lib/apt/lists/*

# Install requests
RUN pip3 install requests

# Create the directory structures
RUN mkdir /Log_Viewer

# copy the files required for the application
COPY show_server_log.py /Log_Viewer/
COPY v3_00_Show_Log.py /Log_Viewer/

# Set the working directory for the container
WORKDIR /Log_Viewer/

# Set the entrypoint
ENTRYPOINT ["/Log_Viewer/show_server_log.py"]

# Set default parameters
CMD ["--help"]

