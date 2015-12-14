import notifications.resources.Config as Config
from notifications import app, api
from notifications.resources.Notification import Notification
from jsonschema import validate, exceptions
import sqlite3
from flask import g

class Notification_DB(object):
    database_name = None

    # Reference: http://flask.pocoo.org/docs/0.10/patterns/sqlite3/
    @app.teardown_appcontext
    def teardown_close(self):
        database = Config.db_get()
        Config.db_close(database)

    def query_all(self):
        return_list = []

        try:
            database = Config.db_get()
            db_records = Config.db_execute(
                database=database,
                sql_statement='select key, value from notifications',
                multiple=True
            )
            Config.db_close(database)

            for db_row in db_records:
                return_list.append(db_row[1])
        except Exception as e:
            raise

        return return_list

    def query_one(self, key):
        if key == None\
        or type(key) != int\
        or key < 0:
            raise KeyError('Key must be greater than or equal to zero')

        database = Config.db_get()
        db_records = Config.db_execute(
            database=database,
            sql_statement='select key, value from notifications '+\
                          'where key = ?',
            args=(key,),
            multiple=False
        )
        Config.db_close(database)

        if db_records == None:
            raise IndexError('Notification does not exist.')

        return db_records[1]

    def delete_one(self, key):
        try:
            database = Config.db_get()
            db_records = Config.db_execute(
                database=database,
                sql_statement='delete from notifications '+ \
                              'where key = ?',
                args=(key, )
            )
            database.commit()
            Config.db_close(database)
        except Exception as e:
            raise

        return

    def delete_all(self):
        try:
            database = Config.db_get()
            db_records = Config.db_execute(
                database=database,
                sql_statement='delete from notifications'
            )
            database.commit()
            Config.db_close(database)
        except Exception as e:
            raise
        
        return

    def update_one(self, key, value):
        updated_data = False

        try:
            database = Config.db_get()
            db_records = Config.db_execute(
                database=database,
                sql_statement='update notifications '+ \
                              'set value = ? '+ \
                              'where key = ?',
                args=(value, key)
            )

            database.commit()
            Config.db_close(database)
        except Exception as e:
            print('The exception happend here!', repr(e))
            raise
        
        return

    def insert(self, note):
        try:
            database = Config.db_get()
            db_records = Config.db_execute(
                database=database,
                sql_statement='select ifnull(max(key),0) from notifications',
                multiple=False
            )

            note.identifier = db_records[0] + 1

            db_records = Config.db_execute(
                database=database,
                sql_statement='insert into notifications (key, value) '+ \
                              'values (?, ?)',
                args=(note.identifier, note.dump())
            )

            database.commit()
            Config.db_close(database)
        except Exception as e:
            raise

