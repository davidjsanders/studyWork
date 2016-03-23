#
# Dockerfile
# ----------
# Purpose - build the Docker container image for the Phone device
#           to enable the application to run on any platform that
#           supports Docker.
#
# MAINTAINER David Sanders <dsanders_can@outlook.com>
#
# Revision History
# -----------------------------------------------------------------------------
# Date         | By             | Reason
# -----------------------------------------------------------------------------
# 02 Mar 2016  | D Sanders      | First version. Builds on stage2_phone
#
# Use the base Python image which includes Python3, Flask, and Flask_Restful
# 
FROM dsanderscan/mscit_v3_01_phone
COPY Phone/Control.py /Phone/Phone/
COPY Phone/v3_02_Control.py /Phone/Phone
