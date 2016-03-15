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
    sqlite3 \
&& rm -rf /var/lib/apt/lists/*
RUN pip3 install flask
RUN pip3 install flask-restful
RUN pip3 install uwsgi
RUN pip3 install --upgrade requests
#RUN pip3 install virtualenv
#RUN virtualenv flask
#RUN flask/bin/pip install flask
#RUN flask/bin/pip install flask-restful
#RUN flask/bin/pip install uwsgi
#RUN flask/bin/pip install requests

