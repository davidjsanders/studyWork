"""
    module: main.py
    ------------------------------------------------------------------------
    Author:      David J. Sanders
    Student No:  H00035340
    Last Update: 15 December 2015
    Update:      Revise documentation
    ------------------------------------------------------------------------
    Overivew:    Main application. Enabled using the larger application
                 pattern from the Flask website to enable the app to run using
                 the uWSGI app server and nginx web server in docker.

    Purpose:     Configures the web service routes by adding resources

    Called By:   notifications/__init__.py

    Patterns:    Larger Applications pattern from Flask website (Ronacher,
                 2013)

    References
    ----------
    Ronacher, A., 2013, 'Larger Applications' [ONLINE]. Available at: 
        http://flask.pocoo.org/docs/0.10/patterns/packages/ (Accessed: 04 
        November 2015)
"""
# Import the required modules from the flask_restful package
from flask_restful import Resource, Api, reqparse, abort

# Import the app (flask) and api (flask_restful) contexts
from notifications import app, api

# Import configuration settings
import notifications.resources.Config as Config

# Import the Response Object
from notifications.resources.Response import Response_Object

# Import the Notification Lock Object
from notifications.resources.Notification_Lock import Notification_Lock

# Import the Notification Helper (Routes) Object
from notifications.resources.Notification_Helper import Notification_Helper

# Import the Notification Schema Object
from notifications.resources.Notification_Schema import Notification_Schema

# Import the Notification Pair (Bluetooth emulation) Object
from notifications.resources.Notification_Pair import Notification_Pair

# Import the Notification Pair Schema Object
from notifications.resources.Notification_Pair_Schema \
    import Notification_Pair_Schema

# Import the Notification Objects
from notifications.resources.Notification_Boundary \
    import Notification_All, Notification_One


#
# Configure web service routes
#
api.add_resource(Notification_Schema,
                 '/v1_00/notifications/schema')
api.add_resource(Notification_All,
                 '/v1_00/notifications/<string:controlkey>')
api.add_resource(Notification_One,
                 '/v1_00/notifications/<string:controlkey>/<int:id>')
api.add_resource(Notification_Helper,
                 '/v1_00/')
api.add_resource(Notification_Pair,
                 '/v1_00/pair/<string:controlkey>')
api.add_resource(Notification_Pair_Schema,
                 '/v1_00/pair/schema')
api.add_resource(Notification_Lock, '/v1_00/lock')

