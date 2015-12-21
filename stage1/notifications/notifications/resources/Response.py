"""
    module: Response.py
    ------------------------------------------------------------------------
    Author:      David J. Sanders
    Student No:  H00035340
    Last Update: 15 December 2015
    Update:      Revise documentation
    ------------------------------------------------------------------------
    Overivew:    The class definition for creating HTTP responses.

    Purpose:     Defines a helper class used by many other objects to prepare
                 and return valid HTTP responses.

    Called By:   ** many **

    References
    ----------

"""
# Import the flask components
from flask import Response

# Import JSON
import json

class Response_Object(object):
    '''
Response_Object()
-----------------
The Response_Object class enables HTTP responses to be defined to a common 
standard.
    '''
    def __init__(
        self,
        data,
        status=200,
        success_fail='success',
        message='done',
        mimetype='application/json'
    ):
        '''
__init__(data={}|[]|'', ...)
Initializes the object and passes in at least a stream of data to be returned.
The data can be any type as long as it is JSON serializable; other parameters
can include:
  1. status - the http status code (e.g. 200 - Ok, 400 - bad request, etc.)
  2. success_fail - a single string indicator, e.g. success, fail, warnings, etc
  3. message - a human readable message that should be displayed.
  4. mimetype - the data type of the request response, defaults to json
        '''
        self.response_data = data
        self.response_status = status
        self.response_success_fail = success_fail
        self.response_message = message
        self.response_mimetype = mimetype

    def response(self):
        '''
response()
Builds the http response based on the contents of the object, building a 
response dictionary containing the success_fail state, the message, the status,
and the data. The response dictionary looks like:

{'success':
  {'message':'This is the set of vowels in English',
   'status':'200',
   'data':['a','e','i','o','u']
  }
}

The response then includes the dictionary, status, and mimetype.
        '''
        # Build the dictionary
        return_dict = {self.response_success_fail:
            {"message":self.response_message,
             "status":self.response_status,
             "data":self.response_data
            }}

        # Call the Flask response function to build the response and return it
        return Response(
            json.dumps(return_dict),
            status=self.response_status,
            mimetype=self.response_mimetype)


