"""
    module: Notification_Helper.py
    ------------------------------------------------------------------------
    Author:      David J. Sanders
    Student No:  H00035340
    Last Update: 20 December 2015
    Update:      Add new route for uWSGI statistics
                 Revise documentation
    ------------------------------------------------------------------------
    Overivew:    The helper module returns the routes available to a caller.

    Purpose:     Return a list of routes and the methods that can be used with
                 them. This is used to provide callers with a means of 
                 interrogating the capabilities provided by the microservice
                 as opposed to knowing their capabilities.

    Called By:   ** many **

    References
    ----------

"""
# Import the flask_restful components
from flask_restful import Resource, Api, reqparse, abort

# Import the configuration package
import notifications.resources.Config as Config

# Import the configuration package
import notifications.resources.Config as Config

# Import the notification object to get the URL
from notifications import app, api

# Import the notification lock package to get the URL
from notifications.resources.Notification_Lock import Notification_Lock

# Import the notification schema package to get the URL
from notifications.resources.Notification_Schema import Notification_Schema

# Import the notification response package to get the URL
from notifications.resources.Response import Response_Object

# Import the uWSGI Statistics Object
from notifications.resources.Uwsgi_Statistics import Uwsgi_Statistics

class Notification_Helper(Resource):
    '''
Notification_Helper()
---------------------
The Notification_Helper object provides a means for the notification service to
tell others the routes and methods available for interaction.
    '''

    def get(self):
        '''
get()
-----
The only method available. Returns the data as a JSON dataset.
        '''
        response_object = Response_Object(
            data={'_links':{}},
            message='Available routes (links) for this service'
        )

        ext_mode = False       # Do not include http://server... as this will
                               # be manipulated before returning.

        # Use the application context of the Flask app to be able to call the
        # api.url_for call to generate the URL for a route.
        with app.test_request_context():
            # Link Structure
            # --------------
            # links['_links']['LINK_NAME'] = {     # LINK_NAME = name of link
            #     'identifier':X,                  # X a number
            #     'href':'XXX',                    # A URL
            #     'rel':'links',                   # The rel identifier
            #     'description':'XXX',             # A human readable desc.
            #     'methods':['VERB','VERB',...]}   # List of supported verbs
            #

            # Link 1: The helper
            response_object.response_data['_links']['self'] = {
                'identifier':0,
                'href':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Notification_Helper, _external=ext_mode),
                'rel':'links',
                'description':'Display routes supported by this service.',
                'methods':['GET','OPTIONS','HEAD']}

            # Link 2: The collection of notifications
            response_object.response_data['_links']['notifications'] = {
                'identifier':1,
                'href':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Notification_Helper, _external=ext_mode)+\
                    'notifications/<string:controlkey>',
                'schema':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Notification_Schema, _external=ext_mode),
                'rel':'collection',
                'description':'Display and manipulate the notification list '+\
                    'and post new notifications.',
                'methods':['GET','POST', 'DELETE','OPTIONS','HEAD']}

            # Link 3: The operations on a single notification
            response_object.response_data['_links']['notifications_list'] = {
                'identifier':2,
                'href':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Notification_Helper, _external=ext_mode)+\
                    'notifications/<string:controlkey>/<int:identifier>',
                'rel':'notification',
                'schema':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Notification_Schema, _external=ext_mode),
                'description':'Edit, Delete, or Fetch individual notifications.',
                'methods':['GET','PUT', 'DELETE','OPTIONS','HEAD']}

            # Link 4: The Bluetooth pairing
            response_object.response_data['_links']['notifications_pair'] = {
                'identifier':3,
                'href':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Notification_Helper, _external=ext_mode)+\
                    'pair/<string:controlkey>',
                'rel':'notification',
                'schema':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Notification_Helper, _external=ext_mode)+'pair/schema',
                'description':'Pair with a Bluetooth device.',
                'methods':['GET','POST', 'DELETE','OPTIONS','HEAD']}

            # Link 5: The device lock status
            response_object.response_data['_links']['lock'] = {
                'identifier':4,
                'href':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Notification_Lock, _external=ext_mode),
                'rel':'lock',
                'description':'Device lock',
                'methods':['GET','POST','OPTIONS','HEAD']}

            # Link 6: The unlock link
            response_object.response_data['_links']['unlock'] = {
                'identifier':5,
                'href':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Notification_Lock, _external=ext_mode)+\
                    '?unlock_code=<int:unlock_code>',
                'rel':'lock',
                'description':'Device unlock',
                'methods':['PUT','OPTIONS','HEAD']}

            # Link 7: Get uWSGI statistics
            response_object.response_data['_links']['uwsgi-statistics'] = {
                'identifier':6,
                'href':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Uwsgi_Statistics, _external=ext_mode),
                'rel':'stats',
                'description':'Get statistics for the uWSGI service',
                'methods':['GET','OPTIONS','HEAD']}

        # Return the HTTP response object with data and status. The Response_
        # Object class will create an HTTP Response with the correct data,
        # status code, and mimetype.
        return response_object.response()


