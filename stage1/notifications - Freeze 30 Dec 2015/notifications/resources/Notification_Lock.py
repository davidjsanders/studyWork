"""
    module: Notification_Lock.py
    ------------------------------------------------------------------------
    Author:      David J. Sanders
    Student No:  H00035340
    Last Update: 15 December 2015
    Update:      Revise documentation
    ------------------------------------------------------------------------
    Overivew:    The emulation of locking the device.

    Purpose:     A route which enables the device to be locked, the status
                 of the lock (locked or unlocked) to be obtained, and to be 
                 unlocked. The locked status is maintained in a key/value pair
                 which is persistent.

    Called By:   ** many **

    References
    ----------

"""
# Import the flask_restful components
from flask_restful import Resource, Api, reqparse, abort

# Import the app and api contexts
from notifications import app, api

# Import the configuration package
import notifications.resources.Config as Config

# Import the response object to build HTTP responses
from notifications.resources.Response import Response_Object

# Import the pairing schema
from notifications.resources.Notification_Pair_Schema \
    import Notification_Pair_Schema

# Import JSON, jsonschema, and http requests packages
from jsonschema import validate, exceptions
import json
import requests

class Notification_Lock(Resource):
    '''
Notification_Lock()
------------------
The Notification_Lock object handles routes for get, post, and put on the
device to emulate being locked, being unlocked, and being able to check the lock
status.
    '''
    def process(self, method='GET'):
        '''
process(method='VERB')
The process method is a helper method which is called by the routes and collects
frequently used logic together.
        '''
        response_object = Response_Object(data=None)
        try:
            # GET is used to check the lock status
            if method.upper() == 'GET':
                # Get the current lock status from a K/V pair
                locked = Config.get_key('locked')

                # K/V values are strings. If it's TRUE (i.e. locked) then return
                # locked otherwiser return unlocked.
                if locked.upper() == 'TRUE':
                    response_object.response_data = True
                    response_object.response_message = 'Device is locked.'
                else:
                    response_object.response_data = False
                    response_object.response_message = 'Device is unlocked.'
                
            # POST locks the device, regardless of current status.
            elif method.upper() == 'POST':
                locked = Config.set_key('locked', 'TRUE')
                response_object.response_data = True
                response_object.response_message = 'Device is locked.'

            # PUT unlocks the device BUT only if it's locked. If not currently
            # locked, an error is raised.
            elif method.upper() == 'PUT':
                # Check device IS locked
                if Config.get_key('locked').upper() == 'TRUE':
                    # Parse any arguments provided with the request. This SHOULD
                    # only be required with a PUT request when the unlock code
                    # MUST be passed as JSON data.

                    # Set the __unlock_code to None, so we know if it has NOT 
                    # been passed.
                    __unlock_code = None

                    # Setup the parser to parse the requests
                    parser = reqparse.RequestParser()
                    parser.add_argument('unlock_code', type=int)

                    # Execute the parse
                    return_range = parser.parse_args()

                    # Set the unlock code.
                    __unlock_code = return_range['unlock_code']

                    # Check unlock code is correct.
                    if __unlock_code == None \
                    or __unlock_code != Config.unlock_code:
                        response_object.set_failure(
                            failure_message = 'Unlock code is not correct.',
                            status_code = 403
                        )
                    else:
                        locked = Config.set_key('locked', 'FALSE')
                        response_object.response_data = True
                        response_object.response_message = 'Device is unlocked.'
                # Otherwise report error to caller
                else:
                    response_object.set_failure(
                        failure_message = 'Device is not locked.',
                        status_code = 400
                    )
        # An unknown exception needs to be passed back to the caller.
        except Exception as e:
            response_object.set_failure(
                failure_message = repr(e),
                status_code = 400
            )

        # Return the HTTP response object with data and status. The Response_
        # Object class will create an HTTP Response with the correct data,
        # status code, and mimetype.
        return response_object.response()

    def get(self):
        '''
get() - Is the device locked?
        '''
        return self.process()

    def post(self):
        '''
post() - Lock the device
        '''
        return self.process(method='POST')

    def put(self):
        '''
put() - Unlock the device with a code -> put ? unlock_code=9999
        '''
        return self.process(method='PUT')

