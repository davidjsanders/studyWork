FROM dsanders/pythonbase
#MAINTAINER David Sanders <dsanders_can@outlook.com>
RUN mkdir /gendev
RUN mkdir /gendev/static
RUN mkdir /gendev/common
RUN mkdir /gendev/resources
RUN cd /gendev
COPY app.py /gendev/
COPY __init__.py /gendev/
COPY startup.sh /gendev/
COPY resources/Config.py /gendev/resources/
COPY resources/HelloDavid.py /gendev/resources/
COPY resources/HelloWorld.py /gendev/resources/
COPY resources/Testing.py /gendev/resources/
COPY resources/__init__.py /gendev/resources/
COPY resources/Message.py /gendev/resources/
WORKDIR /gendev/
