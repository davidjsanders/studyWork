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
RUN mkdir /Bluetooth/BluetoothReceiver
RUN mkdir /Bluetooth/BluetoothSender
#
# copy the files required for the application
#
COPY runserver.py /Bluetooth/
COPY startup.sh /Bluetooth/
COPY Bluetooth/Control.py /Bluetooth/Bluetooth/
COPY Bluetooth/__init__.py /Bluetooth/Bluetooth/
COPY Bluetooth/main.py /Bluetooth/Bluetooth/
COPY Bluetooth/PairingDatabase.py /Bluetooth/Bluetooth/
COPY Bluetooth/PairingControl.py /Bluetooth/Bluetooth/
COPY BluetoothReceiver/BroadcastBoundary.py /Bluetooth/BluetoothReceiver/
COPY BluetoothReceiver/__init__.py /Bluetooth/BluetoothReceiver/
COPY BluetoothReceiver/main.py /Bluetooth/BluetoothReceiver/
COPY BluetoothReceiver/PairBoundary.py /Bluetooth/BluetoothReceiver/
#
# Set the working directory for the container
#
WORKDIR /Bluetooth/
