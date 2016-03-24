#
# Dockerfile
# ----------
# Purpose - build the Docker container image for the phone screen.
# MAINTAINER David Sanders <dsanders_can@outlook.com>
# Created - 01 Feb 2016
#
#
FROM debian
# Update core packages
RUN apt-get update
RUN apt-get install -y \
    python3 \
    python3-pip \
    redis-server \
# Install python & clean packages
&& rm -rf /var/lib/apt/lists/*

# Install requests
RUN pip3 install requests

# Install Redis
RUN pip3 install redis

# Create the directory structures
RUN mkdir /Phone_Screen

COPY Phone_Screen.py /Phone_Screen/
COPY v3_00_Phone_Screen.py /Phone_Screen/

# Set the working directory for the container
WORKDIR /Phone_Screen/

# Set the entrypoint
ENTRYPOINT ["python3"]

# Set default parameters
CMD ["/Phone_Screen/Phone_Screen.py"]

