FROM dsanders/pythonbase
#MAINTAINER David Sanders <dsanders_can@outlook.com>
RUN mkdir /notes
RUN mkdir /notes/notes
RUN mkdir /notes/notes/static
RUN mkdir /notes/notes/templates
RUN mkdir /notes/notes/resources
#RUN cd /notes
#
# copy notes/ files
#
COPY startup.sh /notes/
COPY runserver.py /notes/
#
# copy notes/notes/ files
#
COPY notes/__init__.py /notes/notes/
COPY notes/main.py /notes/notes/
COPY notes/resources/Config.py /notes/notes/resources/
COPY notes/resources/Notifications.py /notes/notes/resources/
COPY notes/resources/Lock.py /notes/notes/resources/
#WORKDIR /notes/
WORKDIR /
