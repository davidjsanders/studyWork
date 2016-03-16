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
#
# Use the base Python image which includes Python3, Flask, Flask_Restful, and
# 
FROM dsanderscan/pythonbase
#
# Create the directory structures
RUN mkdir /Log_Viewer
#
# copy the files required for the application
#
COPY show_server_log.py /Log_Viewer/
#
# Set the working directory for the container
#
WORKDIR /Log_Viewer/
