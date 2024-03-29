"""
    module: Response.py
    ------------------------------------------------------------------------
    Author:      David J. Sanders
    Student No:  H00035340
    Last Update: 22 December 2015
    Updates
    ------------------------------------------------------------------------
    22 Dec 2015: Update to include additional functionality - set error and
                 set warning
    22 Dec 2015: Added None as a default to data
    15 Dec 2015: Revise documentation
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
        data=None,
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

    def __str__(self):
        return_text = \
            '\033[1mStatus:\033[0m {0}. '.format(
            self.response_status,
        )
        return_text += \
            '\033[1mIndicator:\033[0m {0}. '.format(
            self.response_success_fail
        )
        return_text += \
            '\033[1mMimetype:\033[0m {0}. '.format(
            self.response_mimetype
        )+'\n'
        return_text += \
            '\033[1mMessage:\033[0m {0}. '.format(
            self.response_message
        )+'\n'
        return_text += \
            '\033[1mData:\033[0m {0}.'.format(str(self.response_data))
        return return_text

    def set_failure(
        self,
        failure_message='An error occurred',
        status_code=400,
        caller="UNK",
        step=None
    ):
        self.response_status = status_code
        self.response_message = failure_message
        self.response_success_fail = 'error'
        self.response_data = None # Clear any data
        if step != None:
            self.response_message += ' Service notification: error at '+\
                                     '{0}:{1}'.format(caller,step)

    def set_warning(
        self,
        warning_message='Warnings occurred',
        status_code=400,
        caller="UNK",
        step=None
    ):
        self.response_status = status_code
        self.response_message = warning_message
        self.response_success_fail = 'warning'
        self.response_data = None # Clear any data
        if step != None:
            self.response_message += ' Service notification: error at '+\
                                     '{0}:{1}'.format(caller,step)

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

        # Debug to console - uncomment below
        print(str(self))

        # Call the Flask response function to build the response and return it
        return Response(
            json.dumps(return_dict),
            status=self.response_status,
            mimetype=self.response_mimetype)


