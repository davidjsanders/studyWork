"""
    module: Uwsgi_Statistics.py
    ------------------------------------------------------------------------
    Author:      David J. Sanders
    Student No:  H00035340
    Last Update: 20 December 2015
    Update:      Created
    ------------------------------------------------------------------------
    Overivew:    .

    Purpose:     .

    Called By:   ** many **

    References
    ----------
"""
# Import the configuration package
import notifications.resources.Config as Config

# Import the flask_restful components
from flask_restful import Resource, Api, reqparse, abort

# Import the app and api contexts
from notifications import app, api

# Import the response object to build HTTP responses
from notifications.resources.Response import Response_Object

# Import JSON and http requests packages
import json
import requests

#
# Object for statistics
#
class Uwsgi_Statistics(Resource):
    def get(self):
        # Set the default return flags to show success; exceptions will 
        # change these as required.
        return_message = 'Statistics from uwsgi server'
        return_status = 200
        return_success_fail = 'success'
        return_data = ''
        
        try:
            stat_server = 'http://localhost:9191/'
            r = requests.get(stat_server)
            if r.status_code != 200:
                return_message = 'An error occured due to a return status of '+\
                                 str(r.status_code)
                return_success_fail = 'error'
                return_status = r.status_code
            else:
                return_data = r.json()
        except Exception as e:
            return_message = 'An error occured. '+\
                             repr(e)
            return_success_fail = 'error'
            return_status = 400

        # Return the HTTP response object with data and status. The Response_
        # Object class will create an HTTP Response with the correct data,
        # status code, and mimetype.
        return Response_Object(
                return_data,
                return_status,
                return_success_fail,
                return_message
            ).response()

