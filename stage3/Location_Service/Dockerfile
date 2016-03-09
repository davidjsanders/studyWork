#
# Dockerfile
# ----------
# Purpose - build the Docker container image for the Location Service
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
FROM dsanderscan/mscit_stage2_location_service
COPY Location_Service/main.py /Location_Service/Location_Service/
COPY Location_Service/Check_Control.py /Location_Service/Location_Service/
COPY Location_Service_Boundary/Check_Boundary.py /Location_Service/Location_Service_Boundary/
#
# Set the working directory for the container
#
WORKDIR /Location_Service/
# Set the entrypoint
ENTRYPOINT ["/bin/bash"]
# Set default parameters
CMD ["/Location_Service/startup.sh"]
