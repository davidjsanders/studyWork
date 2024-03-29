from notes import app,api
from flask_restful import Resource, request, reqparse
from flask import abort, url_for
import sqlite3
import requests
import notes.resources.Config as Config
import sys

class Notifications(Resource):
    def get(self):
        try:
            return_list = []

            db_connection = sqlite3.connect(Config.database_connection)
            db_cursor = db_connection.cursor()
            db_cursor.execute(
                'select id, note, action, sensitivity from notifications'
            )
            db_records = db_cursor.fetchall()
            for db_row in db_records:
                return_list.append({
                 'id':db_row[0],
                 'note':db_row[1],
                 'action':db_row[2],
                 'sensitivity':db_row[3],
                 'href':api.url_for(
                     NotificationGetter,
                     id = db_row[0],
                     _external=True),
                 'rel':'self'
                })

        except Exception as e:
            return {'error':repr(e)}
        finally:
             db_cursor.close()
             db_connection.close()
        
        return {'notifications':return_list}

class NotificationsClear(Resource):
    def delete(self):
        try:
            return_list = []

            db_connection = sqlite3.connect(Config.database_connection)
            db_cursor = db_connection.cursor()
            db_cursor.execute(
                'delete from notifications'
            )
            db_connection.commit()
        except Exception as e:
            return {'error':repr(e)}
        finally:
             db_cursor.close()
             db_connection.close()
        
        return {'notifications':[]}

class NotificationGetter(Resource):
    def get(self, id):
        if Config.locked:
            return {'notice':'unlock device first'}
        try:
            return_list = {'notification':''}

            db_connection = sqlite3.connect(Config.database_connection)
            db_cursor = db_connection.cursor()
            db_cursor.execute(
                'select note, action, sensitivity from notifications '+ \
                'where id = ?', \
                (id, )
            )
            db_records = db_cursor.fetchall()
            return_list['notification'] = {
                'note':db_records[0][0],
                'action':db_records[0][1],
                'sensitivity':db_records[0][2]
            }
        except IndexError:
            abort(404)
        except Exception as e:
            return_list = {'error':repr(e)}
        finally:
             db_cursor.close()
             db_connection.close()
        
        return return_list

    def put(self, id):
        try:
            return_list = []
            database_opened = False
            updated_data = False

            tempCall = NotificationGetter()
            return_list = tempCall.get(id)

            if return_list == None:
                abort(404)

            parser = reqparse.RequestParser()
            parser.add_argument('note', type=str)
            parser.add_argument('action', type=str)
            parser.add_argument('sensitivity', type=str)
            args = parser.parse_args()

            for k, v in args.items():
                if not v == None:
                    return_list['notification'][0][k] = v
                    updated_data = True

            if not updated_data:
                pass
            else:
                database_opened = True

            db_connection = sqlite3.connect(Config.database_connection)
            db_cursor = db_connection.cursor()
            db_cursor.execute( \
                'update notifications '+ \
                'set note = ?, action = ?, sensitivity = ? '+ \
                'where id = ?', \
                (return_list['notification'][0]['note'], \
                 return_list['notification'][0]['action'], \
                 return_list['notification'][0]['sensitivity'], \
                 id, ) \
            )
            db_connection.commit()
        except IndexError:
            abort(404)
        except Exception as e:
            return_list = {'error':repr(e)}
        finally:
            if database_opened:
                db_cursor.close()
                db_connection.close()

        return return_list

    def delete(self, id):
        try:
            return_list = []
            database_opened = False
            updated_data = False

            tempCall = NotificationGetter()
            return_list = tempCall.get(id)

            if return_list == None:
                abort(404)

            db_connection = sqlite3.connect(Config.database_connection)
            db_cursor = db_connection.cursor()
            db_cursor.execute(
                'delete from notifications where id = ?', (id,)
            )
            db_connection.commit()
        except Exception as e:
            return {'error':repr(e)}
        finally:
             if database_opened:
                 db_cursor.close()
                 db_connection.close()
        
        return {'notification':[]}

class NotificationAdder(Resource):
    def post(self):
        try:
            insert_list = {
                'notification':{
                    'note':'',
                    'sensitivity':'',
                    'action':''
                }
            }

            database_opened = False
            updated_data = False

            parser = reqparse.RequestParser()
            parser.add_argument('note', 
                                type=str,
                                required=True,
                                help='note must be prodived')
            parser.add_argument('action', 
                                type=str,
                                required=True,
                                help='action must be prodived')
            parser.add_argument('sensitivity', type=str)
            args = parser.parse_args()

            for k, v in args.items():
                if not v == None:
                    insert_list['notification'][k] = v
                    updated_data = True

            database_opened = True

            db_connection = sqlite3.connect(Config.database_connection)
            db_cursor = db_connection.cursor()
            db_cursor.execute( \
                'insert into notifications '+ \
                'values (null, ?, ?, ?)', \
                (insert_list['notification']['note'], \
                 insert_list['notification']['action'], \
                 insert_list['notification']['sensitivity']) \
            )
            insert_list['notification']['id'] = db_cursor.lastrowid
            db_connection.commit()
        except Exception as e:
            insert_list = {'error':repr(e)}
        finally:
            if database_opened:
                db_cursor.close()
                db_connection.close()

        return insert_list
