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
FROM dsanderscan/mscit_v3_00_base
#
# Create the directory structures
RUN mkdir /Bluetooth
RUN mkdir /Bluetooth/Bluetooth
RUN mkdir /Bluetooth/BluetoothBoundary
RUN mkdir /Bluetooth/Bluetooth_Config_Boundary
RUN mkdir /Bluetooth/Bluetooth_Config_Control
RUN mkdir /Bluetooth/datavolume
#
# copy the files required for the application
#
COPY runserver.py /Bluetooth/
COPY startup.sh /Bluetooth/
COPY Bluetooth/__init__.py /Bluetooth/Bluetooth/
COPY Bluetooth/main.py /Bluetooth/Bluetooth/
#
# Boundary
#
COPY Bluetooth_Boundary/__init__.py /Bluetooth/Bluetooth_Boundary/
COPY Bluetooth_Boundary/main.py /Bluetooth/Bluetooth_Boundary/
COPY Bluetooth_Boundary/Broadcast_Boundary.py /Bluetooth/Bluetooth_Boundary/
COPY Bluetooth_Boundary/Pair_Boundary.py /Bluetooth/Bluetooth_Boundary/
#
# Control
#
COPY Bluetooth/Control.py /Bluetooth/Bluetooth/
COPY Bluetooth/v3_00_Control.py /Bluetooth/Bluetooth/
#
COPY Bluetooth/Pairing_Database.py /Bluetooth/Bluetooth/
COPY Bluetooth/v3_00_Pairing_Database.py /Bluetooth/Bluetooth/
#
COPY Bluetooth/Pairing_Control.py /Bluetooth/Bluetooth/
COPY Bluetooth/v3_00_Pairing_Control.py /Bluetooth/Bluetooth/
#
COPY Bluetooth/Broadcast_Control.py /Bluetooth/Bluetooth/
COPY Bluetooth/v3_00_Broadcast_Control.py /Bluetooth/Bluetooth/
#
#
# Config Boundary 
#
COPY Bluetooth_Config_Boundary/main.py /Bluetooth/Bluetooth_Config_Boundary/
COPY Bluetooth_Config_Boundary/Config_Logger_Boundary.py /Bluetooth/Bluetooth_Config_Boundary/
COPY Bluetooth_Config_Boundary/Config_Output_Boundary.py /Bluetooth/Bluetooth_Config_Boundary/
#
# Config Control 
#
COPY Bluetooth_Config_Control/Config_Output_Control.py /Bluetooth/Bluetooth_Config_Control/
COPY Bluetooth_Config_Control/v3_00_Config_Output_Control.py /Bluetooth/Bluetooth_Config_Control/
#
COPY Bluetooth_Config_Control/Config_Logger_Control.py /Bluetooth/Bluetooth_Config_Control/
COPY Bluetooth_Config_Control/v3_00_Config_Logger_Control.py /Bluetooth/Bluetooth_Config_Control/
#
# Set the working directory for the container
#
WORKDIR /Bluetooth/
ENTRYPOINT ["/bin/bash"]        # Set the entrypoint
CMD ["/Bluetooth/startup.sh"]   # Set default parameters
#
# Create the symbolic link to the base library
#
RUN ln -s /base_lib /Bluetooth/base_lib

