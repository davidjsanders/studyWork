from flask_restful import Resource, Api, reqparse, abort
from notifications import app, api

import notifications.resources.Config as Config
from notifications.resources.Notification import Notification
from notifications.resources.Response import Response_Object
#from notifications.resources.Notification_Helper import Notification_Helper
from notifications.resources.Notification_Schema import Notification_Schema
from notifications.resources.Notification_Boundary \
    import Notification_All, Notification_One

from jsonschema import validate, exceptions
import json
import sqlite3

class Notification_Helper(Resource):
    def get(self):
#        port_number = "5000"
        ext_mode = False
        links = {'_links':{}}
        return_status = 200

        with app.test_request_context():
            links['_links']['self'] = {
                'identifier':0,
                'href':'http://'+Config.server_name+':'+Config.port_number+\
                    api.url_for(Notification_Helper, _external=ext_mode),
                'rel':'links',
                'description':'Display routes supported by this service.',
                'methods':['GET','OPTIONS','HEAD']}

            links['_links']['notifications'] = {
                'identifier':1,
                'href':'http://'+Config.server_name+':'+Config.port_number+\
                    api.url_for(Notification_Helper, _external=ext_mode)+\
                    'notifications/<string:controlkey>',
                'schema':'http://'+Config.server_name+':'+Config.port_number+\
                    api.url_for(Notification_Schema, _external=ext_mode),
                'rel':'collection',
                'description':'Display and manipulate the notification list '+\
                    'and post new notifications.',
                'methods':['GET','POST', 'DELETE','OPTIONS','HEAD']}

            links['_links']['notifications_list'] = {
                'identifier':2,
                'href':'http://'+Config.server_name+':'+Config.port_number+\
                    api.url_for(Notification_Helper, _external=ext_mode)+\
                    'notifications/<string:controlkey>/<int:identifier>',
                'rel':'notification',
                'schema':'http://'+Config.server_name+':'+Config.port_number+\
                    api.url_for(Notification_Schema, _external=ext_mode),
                'description':'Edit, Delete, or Fetch individual notifications.',
                'methods':['GET','PUT', 'DELETE','OPTIONS','HEAD']}

        return Response_Object(links, return_status).response()

api.add_resource(Notification_Schema,
                 '/v1_00/notifications/schema')
api.add_resource(Notification_All,
                 '/v1_00/notifications/<string:controlkey>')
api.add_resource(Notification_One,
                 '/v1_00/notifications/<string:controlkey>/<int:id>')
api.add_resource(Notification_Helper,
                 '/v1_00/')
