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
        response_object = Response_Object(
            message = 'Statistics from uwsgi server.'
        )
        try:
            stat_server = 'http://localhost:9191/'
            r = requests.get(stat_server)
            if r.status_code != 200:
                response_object.raise_for_status()
            else:
                response_object.response_data = r.json()
        except requests.exceptions.HTTPError as he:
            response_object.set_failure(
                failure_message = 'An HTTP error occured. '+str(he),
                status_code = he.response.status_code
            )
        except requests.exceptions.ConnectionError as ce:
            response_object.set_failure(
                failure_message = 'A connection error occured. '+str(ce)+'. '\
                    'Please Note: stats are only supported when running the '+\
                    'app on uWSGI.',
                status_code = 500
            )
        except Exception as e:
            response_object.set_failure(
                failure_message = 'An error occured. '+repr(e),
                status_code = 500
            )

        # Return the HTTP response object with data and status. The Response_
        # Object class will create an HTTP Response with the correct data,
        # status code, and mimetype.
        return response_object.response()

