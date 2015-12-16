"""
    module: Notification_DB.py
    ------------------------------------------------------------------------
    Author:      David J. Sanders
    Student No:  H00035340
    Last Update: 15 December 2015
    Update:      Revise documentation
    ------------------------------------------------------------------------
    Overivew:    The persistence layer for notification objects.

    Purpose:     Defines the database members, functions, and operations for the 
                 Notification 'class'

    Called By:   n/a

    References
    ----------

"""
# Import the configuration package
import notifications.resources.Config as Config

# Import the app and api contexts
from notifications import app, api

# Import the notification class
from notifications.resources.Notification import Notification

# Import jsonschema validation and exception functions
from jsonschema import validate, exceptions

# Import SQLite3 for persistence. Could be anything, e.g. redis
import sqlite3

#
# The Notification_DB object.
#
class Notification_DB(object):
    database_name = None

    # Reference: http://flask.pocoo.org/docs/0.10/patterns/sqlite3/
    # The decorator app.teardown_appcontext is fired whenever Flask knows it
    # is done with a request. So, we make sure any database activity is closed
    # properly.
    #
    @app.teardown_appcontext
    def teardown_close(self):
        database = Config.db_get()
        Config.db_close(database)

    # Query all notifications from the database with no qualifiers
    def query_all(self):
        '''
query_all()
Selet all notifications in the database.
        '''
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

    # Query one specific notification from the database
    def query_one(self, key):
        '''
query_one(key=the_key)
Select one notification in the database where key equals the_key. Key MUST be
an integer.
        '''
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
        '''
delete_one(key=the_key)
Delete one notification from the database where key equals the_key. Key MUST be
an integer.
        '''
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
        '''
delete_all()
Delete all notifications in the database.
        '''
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
        '''
update_one(key=the_key, value=the_value)
Update one notification in the database where key equals the_key and set its
value to the_value (e.g. {"notification":"...",...} - IE it must be a string of
JSON data!). Key MUST be an integer.
        '''
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
        '''
insert_one(note=note_object)
Insert a notification in the database. NOTE an object is being passed NOT a
key and string value.
        '''
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

