from notes import app,api
from flask_restful import Resource
from flask import request
from marshmallow import Schema, fields, ValidationError
import sqlite3
import notes.resources.Config as Config
from notes.resources.Persist import Persistance
from notes.resources.Mode import ModeGet

class Notifications(Resource):
    def get(self):
        #
        # If locked AND mode is set to 1 (no notifications when locked)
        # then return nothing.
        #
        app_mode = Config.get_app_mode()
        lock_mode = Config.get_lock()

        if lock_mode \
        and app_mode == Config.app_mode_no_notifications:
            return {'notifications':[]}

        try:
            notification_list = []
            persist = Persistance()
            for db_row in persist.fetch_all(Config.database_connection):
                notification = Config.Note()
                notification.load(db_row[0], NotificationGetter, Notifications)

                append_notification = False

                if app_mode == Config.app_mode_all_notifications:
                    append_notification = True
                else:
                    if lock_mode \
                    and app_mode == Config.app_mode_no_sensitive \
                    and notification.sensitivity.upper() == 'HIGH':
                        append_notification = False
                    else:
                        append_notification = True

                if append_notification:
                    notification_list.append(notification.json())
        except Exception as e:
            return {'error':repr(e)}
        
        return {'notifications':notification_list}

    def delete(self):
        persist = Persistance()
        return persist.clear_all(Config.database_connection)

class NotificationGetter(Resource):
    def get(self, id):
        if Config.locked:
            return {'notice':'unlock device first'}
        try:
            notification = Config.Note()
            notification.load(id, NotificationGetter, Notifications)
            return_list = {'notification':notification.json()}
        except Exception as e:
            return_list = {'error':repr(e)}
        
        return return_list

    def put(self, id):
        try:
            return_list = []
            new_data = request.get_json()

            existing_notification = Config.Note()
            existing_notification.load(id, NotificationGetter, Notifications)
            existing_notification.update(new_data)
            existing_notification.save()
            return_list = existing_notification.json()
        except TypeError as e:
            return_list = {'error':'Type error in put - '+  \
                           repr(e)+'. At step '+str(step) + \
                           'Note is '+repr(existing_notification) + '. ' + \
                           'New Note is '+repr(new_data) + \
                           'JSON is ' + repr(json_data) \
                          }, 400
        except Exception as e:
            return_list = {'error':repr(e)}, 400

        return return_list

    def delete(self, id):
        try:
            notification = Config.Note()
            notification.load(id, NotificationGetter, Notifications)
            notification.delete()
            notification = Config.Note()
        except ValidationError as e:
            return {'error':repr(e)}, 400
        except Exception as e:
            return {'error':repr(e)}, 400

        return {'notification':[]}

class NotificationAdder(Resource):
    def post(self):
        try:
            notification = Config.NoteSchema(strict=True) \
                .load(request.get_json()).data
            notification.save()
            notification.define_links(
                NotificationGetter,
                Notifications)
        except ValidationError as e:
            return {'error':repr(e)}, 400
        except Exception as e:
            return {'error':repr(e)}, 400

        return {'notification':notification.json()}


