#
# Dockerfile
# ----------
# Purpose - build the Docker container image for the Bluetooth device
#           to enable the application to run on any platform that
#           supports Docker.
#
# MAINTAINER David Sanders <dsanders_can@outlook.com>
#
# Revision History
# -----------------------------------------------------------------------------
# Date         | By             | Reason
# -----------------------------------------------------------------------------
# 24 Jan 2015  | D Sanders      | First version.
#
#
# Use the base Python image which includes Python3, Flask, Flask_Restful, and
# 
FROM dsanderscan/pythonbase
#
# Create the directory structures
RUN mkdir /Bluetooth
RUN mkdir /Bluetooth/Bluetooth
RUN mkdir /Bluetooth/BluetoothBoundary
RUN mkdir /Bluetooth/BluetoothSender
RUN mkdir /Bluetooth/Bluetooth_Config_Boundary
RUN mkdir /Bluetooth/Bluetooth_Config_Control
#
# copy the files required for the application
#
COPY runserver.py /Bluetooth/
COPY startup.sh /Bluetooth/
COPY Bluetooth/__init__.py /Bluetooth/Bluetooth/
COPY Bluetooth/main.py /Bluetooth/Bluetooth/
COPY Bluetooth/Control.py /Bluetooth/Bluetooth/
COPY Bluetooth/Pairing_Database.py /Bluetooth/Bluetooth/
COPY Bluetooth/Pairing_Control.py /Bluetooth/Bluetooth/
COPY Bluetooth/Broadcast_Control.py /Bluetooth/Bluetooth/
COPY Bluetooth_Boundary/__init__.py /Bluetooth/Bluetooth_Boundary/
COPY Bluetooth_Boundary/main.py /Bluetooth/Bluetooth_Boundary/
COPY Bluetooth_Boundary/Broadcast_Boundary.py /Bluetooth/Bluetooth_Boundary/
COPY Bluetooth_Boundary/Pair_Boundary.py /Bluetooth/Bluetooth_Boundary/
#
COPY Bluetooth_Config_Boundary/main.py /Bluetooth/Bluetooth_Config_Boundary/
COPY Bluetooth_Config_Boundary/Config_Logger_Boundary.py /Bluetooth/Bluetooth_Config_Boundary/
COPY Bluetooth_Config_Boundary/Config_Output_Boundary.py /Bluetooth/Bluetooth_Config_Boundary/
COPY Bluetooth_Config_Control/Config_Output_Control.py /Bluetooth/Bluetooth_Config_Control/
COPY Bluetooth_Config_Control/Config_Logger_Control.py /Bluetooth/Bluetooth_Config_Control/
#
# Set the working directory for the container
#
WORKDIR /Bluetooth/
