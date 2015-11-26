from notifications import app, api
from notifications.resources.Notification import Notification
from jsonschema import validate, exceptions
import sqlite3

class Notification_DB(object):
    database_name = 'datavol/notifications.db'

    def query_one(self, key):
        if key == None\
        or type(key) != int\
        or key < 0:
            raise KeyError('Key must be greater than or equal to zero')

        return_data = ''
        database_opened = False
        updated_data = False

        db_connection = sqlite3.connect(self.database_name)
        db_cursor = db_connection.cursor()
        database_opened = True
        db_cursor.execute(
            'select key, value from notifications where key = ?',
            (key,) \
        )

        db_records = db_cursor.fetchone()
        if db_records == None:
            raise IndexError('Notification does not exist.')

        db_cursor.close()
        db_connection.close()
        
        return db_records[1]


    def query_all(self):
        database_opened = False
        cursor_opened = False
        return_list = []

        try:
            db_connection = sqlite3.connect(self.database_name)
            database_opened = True

            db_cursor = db_connection.cursor()
            cursor_opened = True

            db_cursor.execute(
                'select key, value from notifications'
            )
            db_records = db_cursor.fetchall()
            for db_row in db_records:
                return_list.append(db_row[1])
        except Exception as e:
            raise
        finally:
             if cursor_opened:
                 db_cursor.close()
             if database_opened:
                 db_connection.close()

        return return_list


    def delete_one(self, key):
        try:
            database_opened = False
            updated_data = False

            db_connection = sqlite3.connect(self.database_name)
            db_cursor = db_connection.cursor()
            db_cursor.execute(
                'delete from notifications where key = ?', (key,)
            )
            db_connection.commit()
        except Exception as e:
            raise
        finally:
            if database_opened:
                db_cursor.close()
                db_connection.close()
        
        return

    def delete_all(self):
        try:
            database_opened = False
            updated_data = False

            db_connection = sqlite3.connect(self.database_name)
            db_cursor = db_connection.cursor()
            db_cursor.execute(
                'delete from notifications'#, (key,)
            )
            db_connection.commit()
        except Exception as e:
            raise
        finally:
            if database_opened:
                db_cursor.close()
                db_connection.close()
        
        return

    def update_one(self, key, value):
        database_opened = False
        cursor_opened = False
        updated_data = False

        try:
            db_connection = sqlite3.connect(self.database_name)
            database_opened = True
            db_cursor = db_connection.cursor()
            cursor_opened = True

            db_cursor.execute( \
                'update notifications '+ \
                'set value = ? '+ \
                'where key = ?', \
                (value, \
                 key ) \
            )

            db_connection.commit()
        except Exception as e:
            raise
        finally:
            if cursor_opened:
                db_cursor.close()
            if database_opened:
                db_connection.close()
        
        return

    def insert(self, note):
        database_opened = False
        cursor_opened = False

        try:
            db_connection = sqlite3.connect(self.database_name)
            database_opened = True

            db_cursor = db_connection.cursor()
            cursor_opened = True

            db_cursor.execute('select ifnull(max(key),0) from notifications')
            db_records = db_cursor.fetchall()
            note.identifier = db_records[0][0] + 1

            db_cursor.execute( \
                'insert into notifications (key, value) '+ \
                'values (?, ?)', \
                (note.identifier, note.dump()) \
            )
            db_connection.commit()
        except Exception as e:
            raise
        finally:
            if cursor_opened:
                db_cursor.close()
            if database_opened:
                db_connection.close()

