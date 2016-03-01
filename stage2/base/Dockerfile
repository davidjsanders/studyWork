FROM debian
MAINTAINER David Sanders <dsanders_can@outlook.com>
LABEL description="David Sanders, University of Liverpool. Base Image." Version="1.0"
RUN apt-get update && apt-get install -y python3-minimal
RUN apt-get install -y \
    curl \
    nginx \
    openssl \
    python3 \
    python3-pip \
    sqlite3
&& rm -rf /var/lib/apt/lists/*
RUN pip3 install flask
RUN pip3 install flask-restful
RUN pip3 install uwsgi
RUN pip3 install requests
#RUN pip3 install virtualenv
#RUN virtualenv flask
#RUN flask/bin/pip install flask
#RUN flask/bin/pip install flask-restful
#RUN flask/bin/pip install uwsgi
#RUN flask/bin/pip install requests

