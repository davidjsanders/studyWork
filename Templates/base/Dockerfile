FROM ubuntu:14.04
MAINTAINER David Sanders <dsanders_can@outlook.com>
LABEL description="David Sanders, University of Liverpool. Base Image." Version="1.0"
RUN apt-get update
RUN apt-get install -y --fix-missing \
    curl \
    net-tools \
    nginx \
    openssl \
    python3 \
    python3-pip \
    redis-server \
    sqlite3 \
&& rm -rf /var/lib/apt/lists/*
#
# Install additional apps for this module
#
RUN pip3 install flask
RUN pip3 install flask-restful
RUN pip3 install uwsgi
RUN pip3 install --upgrade requests
RUN pip3 install --upgrade redis
#
# Setup the base library
#
RUN mkdir /base_lib
#
# copy the base_lib files
#
COPY __init__.py /base_lib/
COPY Config_Logger.py /base_lib/
COPY v1_00_Config_Logger.py /base_lib/
COPY Environment.py /base_lib/
COPY KVStore.py /base_lib/
COPY Logger.py /base_lib/
COPY Responder.py /base_lib/
#RUN pip3 install virtualenv
#RUN virtualenv flask
#RUN flask/bin/pip install flask
#RUN flask/bin/pip install flask-restful
#RUN flask/bin/pip install uwsgi
#RUN flask/bin/pip install requests

