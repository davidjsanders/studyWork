"""
    module: Notification_Schema.py
    ------------------------------------------------------------------------
    Author:      David J. Sanders
    Student No:  H00035340
    Last Update: 15 December 2015
    Update:      Revise documentation
    ------------------------------------------------------------------------
    Overivew:    The schema for notifications.

    Purpose:     Defines a schema for pairing bluetooth devices. Currently, the
                 schema is held in a file - this needs to change!

    Called By:   ** many **

    References
    ----------

"""
# Import the flask_restful components
from flask_restful import Resource

# Import the config module for configuration information
import notifications.resources.Config as Config

# Import the response object to build HTTP responses
from notifications.resources.Response import Response_Object

# Import json
import json

class Notification_Pair_Schema(Resource):
    '''
Notification_Pair_Schema()
--------------------------
The Notification_Pair_Schema object enables callers and interactors to obtain 
the schema for pairing an emulated device with a Bluetooth device.
    '''
    def get(self):
        ''' get() - Return the schema '''
        response_object = Response_Object()
        try:
            # Load the schema from a file - this needs to change!
            f = open(Config.__pair_schema_filename__,'r')
            response_object.response_data = json.load(f)
            f.close()
        # If somethings goes wrong, return the exception.
        except Exception as e:
            response_object.set_failure(
                failure_message='Fetching schema and an exception '+\
                                'was raised: '+repr(e),
                status_code=500
            )

        # Return the HTTP response object with data and status. The Response_
        # Object class will create an HTTP Response with the correct data,
        # status code, and mimetype.
        return response_object.response()

