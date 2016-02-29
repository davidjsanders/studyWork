FROM ubuntu:14.04
#MAINTAINER David Sanders <dsanders_can@outlook.com>
RUN apt-get update && apt-get install -y python3-minimal
RUN apt-get install -y openssl
RUN apt-get install -y curl
RUN apt-get install -y nginx
RUN apt-get install -y python3-pip
RUN apt-get install -y sqlite3
RUN pip3 install virtualenv
RUN virtualenv flask
RUN flask/bin/pip install flask
RUN flask/bin/pip install flask-restful
RUN flask/bin/pip install uwsgi
RUN flask/bin/pip install requests
RUN flask/bin/pip install -U marshmallow
RUN flask/bin/pip install jsonschema
RUN flask/bin/pip install warlock

