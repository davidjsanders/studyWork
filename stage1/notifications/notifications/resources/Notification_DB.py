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
    def db_close(self, exception=None):
        database = getattr(g, '_database', None)
        if database is not None:
            database.close()

    def db_get(self):
        database = getattr(g, '_database', None)

        if database == None:
            database_name = Config.get_database()
            database = g._database = sqlite3.connect(database_name)

        if database == None:
            raise Exception('Unable to connect to database.')

        return database

    def db_execute(self, sql_statement=None, args=(), multiple=False):
        if sql_statement == None:
            return []

        return_data = self.db_get().execute(sql_statement, args)\
                          .fetchall()

        if not multiple:
            if not return_data == []:
                return_data = return_data[0]

        return return_data

    def query_all(self):
        return_list = []

        try:
            db_records = self.db_execute(
                sql_statement='select key, value from notifications',
                multiple=True
            )

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

        db_records = self.db_execute(
            sql_statement='select key, value from notifications '+\
                          'where key = ?',
            args=(key,),
            multiple=False
        )

        if db_records == None:
            raise IndexError('Notification does not exist.')

        return db_records[1]


    def delete_one(self, key):
        try:
            db_records = self.db_execute(
                sql_statement='delete from notifications '+ \
                              'where key = ?',
                args=(key, )
            )
            self.db_get().commit()
        except Exception as e:
            raise

        return

    def delete_all(self):
        try:
            db_records = self.db_execute(
                sql_statement='delete from notifications'
            )
            self.db_get().commit()
        except Exception as e:
            raise
        
        return

    def update_one(self, key, value):
        updated_data = False

        try:
            db_records = self.db_execute(
                sql_statement='update notifications '+ \
                              'set value = ? '+ \
                              'where key = ?',
                args=(value, key)
            )

            self.db_get().commit()
        except Exception as e:
            print('The exception happend here!', repr(e))
            raise
        
        return

    def insert(self, note):
        try:
            db_records = self.db_execute(
                sql_statement='select ifnull(max(key),0) from notifications',
                multiple=False
            )

            note.identifier = db_records[0] + 1

            db_records = self.db_execute(
                sql_statement='insert into notifications (key, value) '+ \
                              'values (?, ?)',
                args=(note.identifier, note.dump())
            )

            self.db_get().commit()
        except Exception as e:
            raise

