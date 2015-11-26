from flask_restful import Resource, Api, reqparse, abort
from notifications import app, api

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
        port_number = "5000"
        ext_mode = True
        links = {'_links':{}}
        return_status = 200

        with app.test_request_context():
            links['_links']['self'] = {
                'identifier':0,
                'href':api.url_for(Notification_Helper, _external=ext_mode)\
                    .replace('http://localhost/','http://localhost:'+port_number+'/'),
                'rel':'self',
                'description':'Display routes supported by this service.',
                'methods':['GET','OPTIONS','HEAD']}
            links['_links']['notification-schema'] = {
                'identifier':1,
                'href':api.url_for(Notification_Schema, _external=ext_mode)\
                    .replace('http://localhost/','http://localhost:'+port_number+'/'),
                'rel':'schema',
                'description':'Get the schema for the notification object',
                'methods':['GET','PUT','DELETE','OPTIONS','HEAD']}
            links['_links']['notifications'] = {
                'identifier':2,
                'href':(api.url_for(Notification_Helper, _external=ext_mode)+\
                    'notifications')\
                    .replace('http://localhost/','http://localhost:'+port_number+'/'),
                'rel':'schema',
                'description':'Display and manipulate the notification list '+\
                    'and post new notifications.',
                'methods':['GET','POST', 'DELETE','OPTIONS','HEAD']}
            links['_links']['notifications_list'] = {
                'identifier':3,
                'href':(api.url_for(Notification_All, _external=ext_mode)+\
                    '/<int:identifier>')\
                    .replace('http://localhost/','http://localhost:'+port_number+'/'),
                'rel':'schema',
                'description':'Edit, Delete, or Fetch individual notifications.',
                'methods':['GET','OPTIONS','HEAD']}

        return Response_Object(links, return_status).response()

api.add_resource(Notification_All, '/v1_00/notifications')
api.add_resource(Notification_One, '/v1_00/notifications/<int:id>')
api.add_resource(Notification_Schema, '/v1_00/notifications/schema')
api.add_resource(Notification_Helper, '/v1_00/')
