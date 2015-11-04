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
COPY resources/__init__.py /gendev/resources/
COPY resources/Notifications.py /gendev/resources/
COPY resources/Lock.py /gendev/resources/
WORKDIR /gendev/
