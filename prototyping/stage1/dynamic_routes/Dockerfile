FROM dsanders/pythonbase
#MAINTAINER David Sanders <dsanders_can@outlook.com>
RUN mkdir /phonews
RUN mkdir /phonews/static
RUN cd /phonews
COPY smartWatch.py /phonews/
#COPY testWS.sh /phonews/
#COPY README /phonews/
#COPY index.html /phonews/static/
COPY startup.sh /phonews/
WORKDIR /phonews/
