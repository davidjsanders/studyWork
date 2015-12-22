"""
    module: Notification_Pair.py
    ------------------------------------------------------------------------
    Author:      David J. Sanders
    Student No:  H00035340
    Last Update: 15 December 2015
    Update:      Revise documentation
    ------------------------------------------------------------------------
    Overivew:    Emulate Bluetooth pairing.

    Purpose:     Defines a set of behaviours to emulate pairing a device with
                 another Bluetooth device.

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

# Import the pairing Schema
from notifications.resources.Notification_Pair_Schema \
    import Notification_Pair_Schema

# Import JSON, jsonschema, and http requests packages
from jsonschema import validate, exceptions
import json
import requests

class Notification_Pair(Resource):
    '''
Notification_Pair()
-------------------
The Notification_Pair object handles routes for get, post, and delete on the
emulated device, allowing pairing with this device and ONE Bluetooth device.
Get, reports back on pairing status; Post, creates a new pairing; Delete, un-
pairs a device.
    '''
    def process(self, controlkey=None, method='GET'):
        '''
process(controlkey='XXX', method='VERB', pair_url='http://...')
The process method is a helper method which is called by the routes and collects
frequently used logic together.
        '''
        response_object = Response_Object(data=None)
        try:
            schema_context={}

            # Check the control key is provided and matches
            if controlkey == None or not controlkey == Config.controlkey_master:
                raise RuntimeError('Control Key does not match.')

            # GET Method
            # ----------------------------------------------------------------
            # i.e. are we paired? If yes, return Bluetooth device
            if method.upper() == 'GET':
                response_object.response_data = Config.get_key('bluetooth')
                if response_object.response_data == None:
                    response_object.response_message = 'Device is not paired.'
                else:
                    response_object.response_message = 'Paired to {0}'\
                        .format(response_object.response_data)

            # DELETE Method
            # ----------------------------------------------------------------
            # i.e. unpair this device
            elif method.upper() == 'DELETE':
                paired_device = Config.get_key('bluetooth')
                if paired_device == None or paired_device == '':
                    raise RuntimeError('Device is not currently paired.')
                response_object.response_data = Config.set_key('bluetooth','')
                response_object.response_message = \
                    'Bluetooth un-paired from {0}.'.format(paired_device)

            # POST Method
            # ----------------------------------------------------------------
            # i.e. pair this device
            elif method.upper() == 'POST':
                # Extract the raw JSON data from the HTTP request and load it into
                # a dictionary.
                raw_json = reqparse.request.get_data().decode('utf-8')
                json_data = json.loads(raw_json)

                # Get the schema required for Bluetooth pairing
                ## NB: This needs to change. The schema is currently retrieved from
                ##     the notification object when it should be retrieved from the
                ##     Bluetooth device; this will also be a good way to check the
                ##     device actually exists!

                if not 'href' in json_data:
                    raise ValueError('Data passed contains no href for device.')

                # Check the url has a trailing /
                if not json_data['href'][-1] == '/':
                    json_data['href'] += '/'

                # Post the request to the device, adding 'pair' to the URL
                r = requests.post(json_data['href']+'pair')

                # Check the return status for 200 (Ok)
                if not r.status_code == 200:
                    raise Exception('The device was not found. Return status is '+\
                              str(r.status_code)
                          )

                # Load the schema
                raw_schema = str(r.json()['success']['data'])
                schema = json.loads(raw_schema.replace("'",'"'))

                # The raw data passed in the request is validated against the 
                # Bluetooth pairing schema.
                validate(json_data, schema)

                # Form the URL for posting to the bluetooth device
                json_data['href'] += 'bluetooth'
                bluetooth_url = json_data['href']

                # Build a message to the device stating now paired.
                sender = str(Config.server_name)+":"+str(Config.port_number)
                payload = {"sender":sender,
                           "message":"Bluetooth device paired with "+sender}

                # Use http to post the message to the bluetooth device
                r = requests.post(
                    bluetooth_url, data=json.dumps(payload))

                response_object.response_data = \
                    Config.set_key('bluetooth', bluetooth_url)
                response_object.response_message += 'Paired to {0}'\
                    .format(bluetooth_url)



        # Exception Handlers
        # ----------------------------------------------------------------
        # An exception of some kind has occurred.
        except RuntimeError as re:
            response_object.set_failure(
                failure_message = str(re)
            )
        except Exception as e:
            response_object.set_failure(
                failure_message = 'Device issue: '+repr(e)
            )



        # End
        # ----------------------------------------------------------------
        # Return the HTTP response object with data and status. The Response_
        # Object class will create an HTTP Response with the correct data,
        # status code, and mimetype.
        return response_object.response()


    def get(self, controlkey=None):
        '''get(controlkey='XXX') - Find out if the device is paired'''
        # Call the helper and process the GET
        return self.process(controlkey=controlkey, method='GET')


    def delete(self, controlkey=None):
        '''delete(controlkey='XXX') - Un-pair the device'''
        # Call the helper and process the DELETE
        return self.process(controlkey=controlkey, method='DELETE')


    def post(self, controlkey=None):
        '''post(controlkey='XXX') - Pair the device'''
        # Call the helper and process the POST
        return self.process(controlkey=controlkey,method='POST')

