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
FROM debian                                   # Base Debian Linux image
RUN apt-get update                            # Update core packages
RUN apt-get install -y \
    python3 \
    python3-pip \
&& rm -rf /var/lib/apt/lists/*                # Install python & clean packages
RUN pip3 install requests                     # Install requests
RUN mkdir /Log_Viewer                         # Create the directory structures
COPY show_server_log.py /Log_Viewer/          # copy the files required for the application
WORKDIR /Log_Viewer/                          # Set the working directory for the container
ENTRYPOINT ["/Log_Viewer/show_server_log.py"] # Set the entrypoint
CMD ["--help"]                                # Set default parameters
