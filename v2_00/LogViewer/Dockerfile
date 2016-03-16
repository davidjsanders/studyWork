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
# 05 Mar 2016  | D Sanders      | First stage 3 version, based on stage 2.
#
# Use the stage 2 container image
FROM dsanderscan/mscit_stage2_log_viewer

# copy the files required for the application
COPY show_server_log.py /Log_Viewer/

# Set the working directory for the container
#WORKDIR /Log_Viewer/

# Set the entrypoint
#ENTRYPOINT ["/Log_Viewer/show_server_log.py"]

# Set default parameters
#CMD ["--help"]

