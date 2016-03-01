#
# Dockerfile
# ----------
# Purpose - build the Docker container image for the phone screen.
# MAINTAINER David Sanders <dsanders_can@outlook.com>
# Created - 01 Feb 2016
#
#
FROM debian
RUN apt-get update                            # Update core packages
RUN apt-get install -y \
    python3 \
    python3-pip \
    redis-server \
&& rm -rf /var/lib/apt/lists/*                # Install python & clean packages
RUN pip3 install requests                     # Install requests
RUN pip3 install redis                        # Install Redis
RUN mkdir /Phone_Screen                       # Create the directory structures
COPY Phone_Screen.py /Phone_Screen/
#COPY Phone_Screen.py /Phone_Screen/           # copy the files required for the application
WORKDIR /Phone_Screen/                        # Set the working directory for the container
ENTRYPOINT ["python3"]  # Set the entrypoint
CMD [" /Phone_Screen/Phone_Screen.py"]        # Set default parameters

