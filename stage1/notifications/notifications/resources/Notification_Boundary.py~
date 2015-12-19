"""
    module: Notification_Boundary.py
    ------------------------------------------------------------------------
    Author:      David J. Sanders
    Student No:  H00035340
    Last Update: 15 December 2015
    Update:      Revise documentation
    ------------------------------------------------------------------------
    Overivew:    The boundary layer for notification objects is used to manage
                 all interactions between a human or machine and notification
                 objects.

    Purpose:     Defines the routes available to humans or machines to interact
                 with the set of notifications. A control key is required to
                 access most routes; at present, this is a simple string which
                 is matched but would normally be stronger (cryptographic keys)
                 and is used to control access.

                 The routes supported are:

                 1. Notification_All - routes accessing ALL notifications
                    a. GET - Get the full set of notifications
                    b. POST - Add a new notification
                    c. DELETE - Delete ALL notifications
                 2. Notification_One - manipulate a SINGLE notification
                    a. GET - Get a notification based on its identifier
                    b. PUT - Update a notification (All fields are updated)
                    c. DELETE - Delete a notification

                 Future Routes would include:
                 1. Notification_All - Enable routes to include ranges, such as
                                       get?from=0&to=10
                 2. Notification_One
                    d. PATCH - Update certain fields of a notification, leaving
                               all others as they are

                 Managing contexts; using the schema functions of Marshmallow,
                 data serialized and returned to the user can be modified based
                 on context (K/V pairs, ontological, etc.). This will be a key
                 factor for stage 2.

    Called By:   ** many **

    References
    ----------
    Dusseault, L., Lab, L., Snell, J (2010), 'RFC 5789 PATCH Method for HTTP'.
        Available at https://tools.ietf.org/html/rfc5789 (Accessed: 19 December 
        2015)

    Fielding, R, Irvine, U.C., Gettys, J., Compaq/W3C, Mogul, J., Compaq, 
        Frystyk, H., W3C/MIT, Masinter, L., Xerox, Leach, P., Microsoft, 
        Berners-Lee, T. (1999), 'Hypertext Transfer Protocol -- HTTP/1.1.' 
        Available at http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html 
        (Accessed: 19 December 2015).

"""
# Import the configuration package
import notifications.resources.Config as Config

# Import the flask_restful components
from flask_restful import Resource, Api, reqparse, abort

# Import the app and api contexts
from notifications import app, api

# Import the notification object
from notifications.resources.Notification import Notification

# Import the response object to build HTTP responses
from notifications.resources.Response import Response_Object

# Import the app and api contexts
from notifications.resources.Notification_DB import Notification_DB

# Import the jsonschema exceptions package to handle validation errors
from jsonschema import exceptions

# Import JSON and http requests packages
import json
import requests

class Notification_All(Resource):
    '''
Notification_All()
------------------
The Notification_All object handles routes for get, post, and delete on the
collection of notifications. GET retrieves all notifications; POST adds a new
notification; and DELETE removes all notifications.
The results returned by the GET route vary depending upon the type of device
being emulated (Android or non-Android and Android pre-lollipop and Android 
post-lollipop) by adapting the context used to serialize data. In the boundary
stage, no adaption is performed - this is all done by the serialization of the
notification object (see Notification.py).
    '''
    def get(self, controlkey=None):
        '''
get(controlKey='XXX')
Get all notifications based on the current context. Notifications are queried
from the database using the entity controller (Notification_DB.py) and initially
marshalled as Notification objects, then dumped to JSON. This approach allows
the schema context to be used to decide which notifications to return (or 
fields)
        '''
        try:
            raw_list=[]        # A raw list used to contain db results
            return_list = []   # The list that will be returned to the user
            schema_context={}  # A schema context to define variable elements
                               # which cause the serialization schema to 
                               # dynamically adapt.

            # The simple control key check. This would typically be stronger
            # cryptographic controls but is not as the focus of this work is
            # privacy and not security.
            if controlkey == None or not controlkey == Config.controlkey_master:
                raise RuntimeError('Control Key does not match.')

            # Set the schema contexts. Find out the type of devices being
            # emulated and then store them in a context dictionary.
            schema_context = Config.set_contexts()

            # Check if the device being emulated is a pre-lollipop Android 
            # device; if it is, and the device is locked, raise an exception to
            # prevent any notifications being displayed.
            Config.check_prelollipop(schema_context)

            # Set the default return flags to show success; exceptions will 
            # change these as required.
            return_message = 'success'
            return_status = 200
            return_success_fail = 'success'

            # Create an instance of the database class
            noteDB = Notification_DB()

            # Execute the query to get ALL notifications
            raw_list = noteDB.query_all()

            # For every result returned from the database object, create a
            # notification object and then serialize it based on the schema
            # context; for example, if a device is being emulated as an Android
            # lollipop device, sensitive (or secure) notifications will not
            # be returned when locked - this is when exceptions.ValidationError
            # is raised and ignored (i.e. not dumped)
            for row in raw_list:
                note = Notification()
                note.load(row)

                try:
                    appending_note = json.loads(
                        note.dump(
                            schema_context=schema_context
                        )
                    )
                    return_list.append(appending_note)
                except exceptions.ValidationError as ve:
                    pass # A validate error means ignore, don't pass data back
                except Exception:
                    raise # Something else happened, so inform caller

            # Check that there are notifications to return.
            if return_list == []:
                return_message = 'No notifications.'
            else:
                return_message = 'notifications found'
        # If validation occurs at the outer try level, then there is bad data
        # in the database, which should not be possible.
        except exceptions.ValidationError as ve:
            return_message = ve.message
            return_status = 400
            return_success_fail = 'error'
        # Runtime error is raised if the device is pre-lollipop Android and
        # locked. This allows us to set the correct return status to HTTP 403 
        # (Forbidden) (Fielding, et al., 1999)
        except RuntimeError as re:
            return_message = str(re)
            return_status = 403
            return_success_fail = 'error'
        # A general exception occurred which was unexpected; therefore, the
        # exception is returned as a failure.
        except Exception as e:
            return_message = repr(e)
            return_status = 400
            return_success_fail = 'error'

        # Return the HTTP response object with data and status. The Response_
        # Object class will create an HTTP Response with the correct data,
        # status code, and mimetype.
        return Response_Object(
                return_list,
                return_status,
                return_success_fail,
                return_message
            ).response()

    def delete(self, controlkey=None):
        '''
delete(controlKey='XXX')
Delete all notifications from the database. No consideration of context is made
and notifications are deleted assuming the user has permission (i.e. knows the
control key). In a production system, the control key would be considerably
stronger to protect API interaction.
        '''

        # Set the default return flags to show success; exceptions will 
        # change these as required.
        return_message = 'Notifications deleted'
        return_status = 200
        return_success_fail = 'success'

        try:
            # The simple control key check. As per GET.
            if controlkey == None or not controlkey == Config.controlkey_master:
                raise RuntimeError('Control Key does not match.')

            # Create a database object
            noteDB = Notification_DB()

            # Delete everything
            noteDB.delete_all()
        # A general exception occurred which was unexpected; therefore, the
        # exception is returned as a failure.
        except Exception as e:
            return_status = 400
            return_message = {'error':'Data not deleted. '+\
                repr(e)}
            return_success_fail = 'error'
        
        # Return the HTTP response object with data and status. The Response_
        # Object class will create an HTTP Response with the correct data,
        # status code, and mimetype.
        return Response_Object(
                [],
                return_status,
                return_success_fail,
                return_message
            ).response()


    def post(self, controlkey=None):
        '''
post(controlKey='XXX')
Create a new notification. At this point, the caller DOES NOT know the
notification ID, so this is a POST interaction rather than a PUT. The posted
data will be validated against the schema and then added to the database.
        '''

        # Set the default return flags to show success; exceptions will 
        # change these as required.
        return_data = []
        return_message = 'Notification created'
        return_status = 201    # Notice status 201 Created not 200 OK
                               # (Fielding, et al., 1999)
        return_success_fail = 'success'

        try:
            # Set the schema context
            schema_context = {}

            # Perform the basic control key check; see GET
            if controlkey == None or not controlkey == Config.controlkey_master:
                raise RuntimeError('Control Key does not match.')

            # Set the contexts for the action
            Config.set_contexts()

            # Extract the raw JSON data from the HTTP request and load it into
            # a dictionary.
            raw_json = reqparse.request.get_data().decode('utf-8')
            json_data = json.loads(raw_json)

            # Create an empty notification object and load the raw data. The
            # load method will perform all validation with any errors being
            # caught by exception handling.
            note = Notification()
            note.load(raw_json, schema_context)

            # When the notification is created, it is valid and so can be
            # persisted in the database.
            noteDB = Notification_DB()
            noteDB.insert(note)

            # Return the data that was passed back to the caller.
            return_data = note.dump(schema_context)

            # Bluetooth
            # ---------
            # If this 'device' has been paired with a bluetooth device, then
            # the notification is passed to the Bluetooth device.

            # Find out if the device is 'paired'
            bluetooth_device = Config.get_key('bluetooth')

            if not bluetooth_device == None:    # The device IS paired
                try:
                    # Create a data payload to pass with the request containing
                    # the sender (a Bluetooth device can be paired more than 
                    # once) and the message
                    payload = {"sender":str(Config.server_name)+":"\
                                   +str(Config.port_number),
                               "message":note.note}

                    # Use http to post the message to the bluetooth device
                    r = requests.post(
                            bluetooth_device, data=json.dumps(payload))

                    # If the response is not 200 (Ok), then raise an exception
                    if r.status_code != 200:
                        raise Exception(str(r.status_code)+str(r.json()))
                except Exception as e:
                    # Ignore any errors trying to get to bluetooth but let the 
                    # caller the know by changing the return state to 'warning'
                    # and including the exception details.
                    return_success_fail = 'warning'
                    return_message += \
                        '. Bluetooth set BUT transmission '+\
                        'failed - could not reach device '+\
                        bluetooth_device + '. Error is '+repr(e)+'.'

        # a ValidationError can be raised by the load method of the notification
        # object; this is caused by badly formatted JSON data, e.g. 
        # {"notes":"Notification",...} instead of {"note":"Notification",...}
        except exceptions.ValidationError as ve:
            return_status = 400
            return_message = {'error':'Data not posted. '+\
                str(ve)}
            return_success_fail = 'error'
            return_data = []
        # a KeyError can be raised by badly formed JSON data, especially when
        # there is no data!
        except KeyError as ke:
            return_status = 400
            return_message = str(ke) + '. No valid key found in: ' +\
                reqparse.request.get_data().decode('utf-8')
            return_success_fail = 'error'
            return_data = []
        # Runtime error is raised if the device is pre-lollipop Android and
        # locked. This allows us to set the correct return status to HTTP 403 
        # (Forbidden) (Fielding, et al., 1999)
        except RuntimeError as re:
            return_status = 403
            return_message = str(re)
            return_success_fail = 'error'
            return_data = []
        # General Exception
        except Exception as e:
            return_status = 400
            return_message = {'error':'Data not posted. '+\
                repr(e)}
            return_success_fail = 'error'
            return_data = []

        # Return the HTTP response object with data and status. The Response_
        # Object class will create an HTTP Response with the correct data,
        # status code, and mimetype.
        return Response_Object(
            return_data,
            return_status,
            return_success_fail,
            return_message
        ).response()

class Notification_One(Resource):
    '''
Notification_One()
------------------
The Notification_One object handles routes for get, post, and delete on a
single notification. GET retrieves the notification; PUT updates an existing
notification; and DELETE removes the existing notification.
The results returned by the GET route vary depending upon the type of device
being emulated as per Notification_All (see above).
    '''

    def get(self, id, controlkey=None):
        '''
get(id=12345, controlKey='XXX')
Get a notification based on an ID and the current context. The notification is 
queried from the database using the entity controller (Notification_DB.py) and 
marshalled as a Notification object, then dumped to JSON. This approach allows
the schema context to be used to decide which notifications to return (or 
fields)
        '''
        try:
            # Set the default return flags to show success; exceptions will 
            # change these as required.
            return_list = []
            return_string = ''
            return_message = 'success'
            return_status = 200
            return_success_fail = 'success'

            # Set the schema context and check the control key, as above
            schema_context={}
            if controlkey == None or not controlkey == Config.controlkey_master:
                raise RuntimeError('Control Key does not match.')

            # Set the schema contexts. Find out the type of devices being
            # emulated and then store them in a context dictionary.
            schema_context = Config.set_contexts()

            # Check if the device being emulated is a pre-lollipop Android 
            # device; if it is, and the device is locked, raise an exception to
            # prevent any notifications being displayed.
            Config.check_prelollipop(schema_context)

            # Create a new notification and db objects
            noteDB = Notification_DB()
            note = Notification()

            # Load the notification from the persistent store / database
            # Data will be automatically validated against the schema by the
            # load method
            note.load(noteDB.query_one(id))

            # Create the JSON dump of the data from the object
            try:
                appending_note = json.loads(
                    note.dump(
                        schema_context=schema_context
                    )
                )
                return_list.append(appending_note)
            # If a validation error occurs then the schema context has prevented
            # the data being returned (see GET in Notification_All)
            except exceptions.ValidationError as ve:
                pass # A validate error means ignore, don't pass data back
            except Exception:
                raise # Something else happened, so inform caller

            # Check if the return list is empty.
            if return_list == []:
                # Check if it's empty because of context
                if 'android' in schema_context\
                and 'locked' in schema_context:
                    # It is, so inform the user that it can't be shown with a
                    # 403 (Forbidden) status
                    return_message = 'Notification is sensitive and cannot '+\
                        'be displayed because device is locked.'
                    return_status = 403
                else:
                    # Otherwise return a 404 - Not found status although we
                    # should NEVER reach here as the load will return an Index
                    # Error if not found.
                    return_message = 'Notification not found.'
                    return_status = 404
                # In either case, set the status to error
                return_success_fail = 'error'

            # Ignore anythin else and return only the first row
            return_list = return_list[0]

        # IndexError is raised by the load method if the notification cannot
        # be found; e.g. get id=1812812812891289128912
        except IndexError as ie:
            return_message = 'The notification '+str(id)+' does not exist.'
            return_status = 404
            return_success_fail = 'error'
        except RuntimeError as re:
            return_message = str(re)
            return_status = 403
            return_success_fail = 'error'
        # A general exception has occurred, so let the caller know.
        except Exception as e:
            return_message = repr(e)
            return_status = 400
            return_success_fail = 'error'
            return_status = 400
        
        # Return the HTTP response object with data and status. The Response_
        # Object class will create an HTTP Response with the correct data,
        # status code, and mimetype.
        return Response_Object(
                return_list,
                return_status,
                return_success_fail,
                return_message
            ).response()

    def put(self, id, controlkey=None):
        '''
put(id=12345, controlKey='XXX')
Update a notification based on an ID and the current context. The notification 
is queried from the database using the entity controller (Notification_DB.py) 
to ensure it exists and then updated based on the data passed. If data is not
passed, then it is left at its original value. PUT was chosen over PATCH, as the
update IS idempotant and is NOT permitted to modify the unique identifier
(Dusseault, et al., 2010). NOTE: Changing the emulation of the device, e.g. from
a lollipop Android device to a pre-lollipop Android device DOES affect data,
removing contents from the sensitivity field.
        '''

        # Set the default return flags to show success; exceptions will 
        # change these as required.
        return_data = []
        return_status = 200
        return_message = 'Notification updated.'
        return_success_fail = 'success'

        try:
            # Set the schema context and check the control key, as above
            schema_context = {}
            if controlkey == None or not controlkey == Config.controlkey_master:
                raise RuntimeError('Control Key does not match.')

            # Set the schema contexts. Find out the type of devices being
            # emulated and then store them in a context dictionary.
            schema_context = Config.set_contexts()

            # Check if the device being emulated is a pre-lollipop Android 
            # device; if it is, and the device is locked, raise an exception to
            # prevent any notifications being displayed.
            Config.check_prelollipop(schema_context)

            # Create a new notification and db objects
            noteDB = Notification_DB()
            note = Notification()

            # Load the existing notification
            note.load(noteDB.query_one(id), schema_context)

            # Create a temporary notification object to contain the new data
            # being passed by the caller
            temp = Notification()

            # Extract the raw JSON data from the HTTP request and load it into
            # a dictionary.
            raw_json = reqparse.request.get_data().decode('utf-8')
            new_note = json.loads(raw_json)

            # Check the raw json data for specific keys. If the keys are found,
            # update the existing notification with the passed data.
            for key in new_note.keys():
                if key == 'note':
                    note.note = new_note[key]
                elif key == 'action':
                    note.action = new_note[key]
                elif key == 'sensitivity':
                    note.sensitivity = new_note[key]
                elif key == 'identifier':
                    pass
                # If another key is found, e.g. "myextension":"new value" then
                # check whether the schema permits additional values by loading
                # the passed data. If it doesn't it will raise an exception. If
                # it does, it is currently ignored.
                else:
                    temp.load(raw_json)

            # Validate the data update by loading it into the temporary
            # notification object. If it fails validation, an exception is 
            # rasied
            temp.load(note.dump(schema_context))

            # If here, then the data is valid, so update the database. This
            # approach is a 'little' convoluted because key/value is used to
            # store the data rather than just telling the notification to
            # persist itself.
            noteDB.update_one(note.identifier, note.dump(schema_context))

            # Pass back the updated notification
            return_data = note.dump(schema_context)
        # IndexError specifies the original notification doesn't exist, so it
        # can't be updated. Therefore, a 404 (not found) error is returned.
        except IndexError as ie:
            return_message = 'The notification '+str(id)+' does not exist.'
            return_status = 404
            return_success_fail = 'error'
        # Any other exception is returned as a 400 (bad request). This typically
        # occurs when data is bad or not provided, e.g. executing a CURL -X PUT
        # but not providing a -d '{"note":"notification",....}', etc.
        except ValueError as e:
            return_status = 400
            return_message = {'error':'Data not posted. The data is '+\
                'badly formed. Please check your data. '+\
                repr(e)}
            return_success_fail = 'error'
            return_data = []
        # Some other exception has occured so let caller know.
        except Exception as e:
            return_status = 400
            return_message = {'error':'Data not posted. '+\
                repr(e)}
            return_success_fail = 'error'
            return_data = []
        
        # Return the HTTP response object with data and status. The Response_
        # Object class will create an HTTP Response with the correct data,
        # status code, and mimetype.
        return Response_Object(
                return_data,
                return_status,
                return_success_fail,
                return_message
            ).response()

    def delete(self, id, controlkey=None):
        '''
delete(id=12345, controlKey='XXX')
Delete a notification based on its ID. The notification is queried from the 
database using the entity controller (Notification_DB.py) to ensure it exists 
and then deleted.
        '''

        try:
            # Set the default return flags to show success; exceptions will 
            # change these as required.
            return_data = []
            return_status = 200
            return_message = 'Notification deleted'
            return_success_fail = 'success'

            # Check the control key, as above
            if controlkey == None or not controlkey == Config.controlkey_master:
                raise RuntimeError('Control Key does not match.')

            # Create a new notification and db objects
            noteDB = Notification_DB()
            note = Notification()

            # Load the notification to check it exists
            note.load(noteDB.query_one(id))

            # Delete the notification
            noteDB.delete_one(id)

        # IndexError means the notification doesn't exist, as above
        except IndexError as ie:
            return_message = 'The notification '+str(id)+' does not exist.'
            return_status = 404
            return_success_fail = 'error'
        # Some other exception has occured so let caller know.
        except Exception as e:
            return_status = 400
            return_message = {'error':'Data not posted. '+\
                repr(e)}
            return_success_fail = 'error'
            return_data = []
        
        # Return the HTTP response object with data and status. The Response_
        # Object class will create an HTTP Response with the correct data,
        # status code, and mimetype. Notice that return_data is left as an
        # empty list.
        return Response_Object(
                return_data,
                return_status,
                return_success_fail,
                return_message
            ).response()


