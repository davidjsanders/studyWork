"""
    module: Notification_Schema.py
    ------------------------------------------------------------------------
    Author:      David J. Sanders
    Student No:  H00035340
    Last Update: 15 December 2015
    Update:      Revise documentation
    ------------------------------------------------------------------------
    Overivew:    The schema for notifications.

    Purpose:     Defines a schema for a notification that dictates the structure
                 of the data. The route supports only one method (GET) which
                 allows the schema to be returned as JSON. The schema is stored
                 as a class variable (i.e. shared across instantiations)

    Called By:   ** many **

    References
    ----------

"""
# Import the flask_restful components
from flask_restful import Resource

# Import the notification object to access the class's schema
from notifications.resources.Notification import Notification

# Import the response object to build HTTP responses
from notifications.resources.Response import Response_Object

class Notification_Schema(Resource):
    '''
Notification_Schema()
---------------------
The Notification_Schema object enables callers and interactors to obtain the
schema for a notification.
    '''
    def get(self):
        ''' get() - Return the schema '''
        response_object = Response_Object(message='Notification schema.')
        # Get the schema from the Notification module
        try:
            # Use the class variable to get the pre-loaded schema. NOTE: this
            # means changes to the schema only occur at initial run - probably
            # should change it!
            response_object.response_data = Notification.__schema__
        except Exception as e:
            response_object.set_failure(
                failure_message = 'An exception occurred: '+repr(e),
                status_code = 500
            )

        # Return the HTTP response object with data and status. The Response_
        # Object class will create an HTTP Response with the correct data,
        # status code, and mimetype.
        return response_object.response()

