FROM dsanders/pythonbase
#MAINTAINER David Sanders <dsanders_can@outlook.com>
RUN mkdir /gendev
RUN mkdir /gendev/static
RUN cd /gendev
COPY gendev.py /gendev/
COPY startup.sh /gendev/
WORKDIR /gendev/
