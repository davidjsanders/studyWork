from flask_restful import Resource, Api, reqparse, abort
from notifications import app, api

from notifications.resources.Notifications import Notification
from jsonschema import validate, exceptions
import json
import sqlite3

class Notification_Boundary_All(Resource):
    database_name = 'datavol/notifications.db'

    def get(self):
        try:
            return_list = []
            return_string = ''

            db_connection = sqlite3.connect(self.database_name)
            db_cursor = db_connection.cursor()
            db_cursor.execute(
                'select key, value from notifications'
            )
            db_records = db_cursor.fetchall()
            for db_row in db_records:
                note = Notification()
                note.load(db_row[1])
                if not note.sensitivity == 'high':
                    return_list.append(note.dump())
                    return_string += ' '+note.dump()
        except exceptions.ValidationError as ve:
            pass
        except Exception as e:
            return {'error':repr(e)}
        finally:
             db_cursor.close()
             db_connection.close()
        
        return return_list

    def post(self):
        return_list = []
        return_status = 201
        database_opened = False
        updated_data = False

        try:
            raw_json = reqparse.request.get_data().decode('utf-8')
            note = Notification()
            note.load(raw_json)

            db_connection = sqlite3.connect(self.database_name)
            db_cursor = db_connection.cursor()
            db_cursor.execute('select ifnull(max(key),0) from notifications')
            db_records = db_cursor.fetchall()
            note.identifier = db_records[0][0] + 1
            db_cursor.execute( \
                'insert into notifications (key, value) '+ \
                'values (?, ?)', \
                (note.identifier, note.dump()) \
            )
            db_connection.commit()
            return_list = note.dump()
        except IndexError:
            abort(404)
        except exceptions.ValidationError as ve:
            return_status = 400
            return_list = {'error':'Data not loaded. '+\
                str(ve.message)}
            abort(return_status, message=return_list)
        except Exception as e:
            return_status = 400
            return_list = {'error':'Data not loaded. '+\
                repr(e)}
            abort(return_status, message=return_list)
        finally:
            if database_opened:
                db_cursor.close()
                db_connection.close()

        return return_list

class Notification_Boundary_One(Resource):
    database_name = 'datavol/notifications.db'

    def get(self, id):
        try:
            return_list = []
            return_string = ''
            database_opened = False
            updated_data = False

            db_connection = sqlite3.connect(self.database_name)
            db_cursor = db_connection.cursor()
            database_opened = True
            db_cursor.execute(
                'select key, value from notifications where key = ?',
                (id,) \
            )
            db_records = db_cursor.fetchall()
            for db_row in db_records:
                note = Notification()
                note.load(db_row[1])
                if not note.sensitivity == 'high':
                    return_list.append(note.dump())
                    return_string += ' '+note.dump()
        except exceptions.ValidationError as ve:
            pass
        except Exception as e:
            return_status = 400
            return_list = {'error':repr(e)}
            abort(return_status, message=return_list)
        finally:
             db_cursor.close()
             db_connection.close()
        
        return return_list

    def put(self, id):
        return_list = []
        database_opened = False
        cursor_opened = False
        updated_data = False

        try:
            raw_json = reqparse.request.get_data().decode('utf-8')
            note = Notification()
            note.load(raw_json)

            db_connection = sqlite3.connect(self.database_name)
            database_opened = True
            db_cursor = db_connection.cursor()
            cursor_opened = True

            db_cursor.execute( \
                'update notifications '+ \
                'set value = ? '+ \
                'where key = ?', \
                (raw_json, \
                 id ) \
            )

            db_connection.commit()
            return_list = note.dump()
        except Exception as e:
            return_status = 400
            return_list = {'error':repr(e)}
            abort(return_status, message=return_list)
        finally:
            if cursor_opened:
                db_cursor.close()
            if database_opened:
                db_connection.close()
        
        return return_list

    def delete(self, id):
        try:
            return_list = []
            database_opened = False
            updated_data = False

            db_connection = sqlite3.connect(self.database_name)
            db_cursor = db_connection.cursor()
            db_cursor.execute(
                'delete from notifications where key = ?', (id,)
            )
            db_connection.commit()
            return_list = {'success':'done.'}
        except Exception as e:
            return_status = 400
            return_list = {'error':repr(e)}
            abort(return_status, message=return_list)
        finally:
            if database_opened:
                db_cursor.close()
                db_connection.close()
        
        return {'message': return_list}

api.add_resource(Notification_Boundary_All, '/v1_00/notifications')
api.add_resource(Notification_Boundary_One, '/v1_00/notifications/<int:id>')

