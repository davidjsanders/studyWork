"""
This module contains key configuration variables used throughout
the package.
"""

#import notes.resources.Config as Config

from marshmallow import Schema, fields, post_load
from notes import app,api
from marshmallow import Schema, fields
from flask import abort
import sqlite3

class Persistance(object):
    def __init__(self):
        pass

    def __repr__(self):
        return '<Persistance()>'

    def fetch_one(self, db_connection, identifier):
        return_dict = None
        try:
            db_connection = sqlite3.connect(db_connection)
            database_opened = True
            db_cursor = db_connection.cursor()
            db_cursor.execute(
                'select note, action, sensitivity from notifications '+ \
                'where id = ?', \
                (identifier, )
            )
            db_records = db_cursor.fetchall()
            if db_records == []:
                abort(404)
#                raise NotFound('The notification ID passed does not exist')
            return_dict = {
                'note':db_records[0][0],
                'action':db_records[0][1],
                'sensitivity':db_records[0][2]
            }
        except Exception as e:
            raise e
        return return_dict

    def fetch_all(self, db_connection):
        try:
            db_connection = sqlite3.connect(db_connection)
            database_opened = True
            db_cursor = db_connection.cursor()
            db_cursor.execute(
                'select id, note, action, sensitivity from notifications'
            )
            while True:
                db_record = db_cursor.fetchone()
                if db_record == None:
                    break
                yield db_record
        except Exception as e:
            print('*** HIT AN EXCEPTION ***')
            print(repr(e))
            raise e
        finally:
            if database_opened:
                db_cursor.close()
                db_connection.close()

    def clear_all(self, db_connection):
        try:
            db_connection = sqlite3.connect(db_connection)
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

    def update(self, notification, db_connection):
        try:
            db_connection = sqlite3.connect(db_connection)
            database_opened = True
            db_cursor = db_connection.cursor()
            db_cursor.execute( \
                'update notifications '+ \
                'set note = ?, action = ?, sensitivity = ? '+
                'where id = ?', \
                (notification.note, \
                 notification.action, \
                 notification.sensitivity, \
                 notification.identifier) \
            )
            identifier = db_cursor.lastrowid
            db_connection.commit()
        except Exception as e:
            print('*** HIT AN EXCEPTION ***')
            print(repr(e))
            raise e
        finally:
            if database_opened:
                db_cursor.close()
                db_connection.close()
        return identifier

    def delete(self, notification, db_connection):
        try:
            database_opened = False
            db_connection = sqlite3.connect(db_connection)
            database_opened = True
            db_cursor = db_connection.cursor()
            db_cursor.execute(
                'delete from notifications where id = ?', (notification.identifier,)
            )
            db_connection.commit()
        except Exception as e:
            raise e
        finally:
             if database_opened:
                 db_cursor.close()
                 db_connection.close()


    def insert(self, notification, db_connection):
        try:
            db_connection = sqlite3.connect(db_connection)
            database_opened = True
            db_cursor = db_connection.cursor()
            db_cursor.execute( \
                'insert into notifications '+ \
                'values (null, ?, ?, ?)', \
                (notification.note, \
                 notification.action, \
                 notification.sensitivity) \
            )
            identifier = db_cursor.lastrowid
            db_connection.commit()
        except Exception as e:
            print('*** HIT AN EXCEPTION ***')
            print(repr(e))
            raise e
        finally:
            if database_opened:
                db_cursor.close()
                db_connection.close()
        return identifier

