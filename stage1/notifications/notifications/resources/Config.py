from notifications import app, api
import sqlite3

port_number = 5000
server_name = 'localhost'

controlkey_master = 'ABC123'

def set_contexts(self, schema=None):
    if schema == None or not type(schema) == dict:
        return {}

    new_schema = {}
    if check_key('android'):
        new_schema['android'] = True
    if check_key('locked'):
        new_schema['locked'] = True
    if check_key('pre-lollipop'):
        new_schema['pre-lollipop'] = True

    if 'pre-lollipop' in schema \
    and 'locked' in schema:
        raise RuntimeError('Device is locked.')

    return new_schema

def check_key(key=None):
    if key==None:
        return False

    database_name = 'datavol/notifications.db'
    try:
        return_data = ''
        database_opened = False
        updated_data = False

        db_connection = sqlite3.connect(database_name)
        db_cursor = db_connection.cursor()
        database_opened = True
        db_cursor.execute(
            'select value from configuration where key = ?',
            (key,) \
        )

        db_records = db_cursor.fetchone()

        db_cursor.close()
        db_connection.close()

        if db_records == None:
            return True # Default to a locked state if database is empty!

        if db_records[0].upper() == 'TRUE':
            return True;
        else:
            return False;
    except Exception as e:
        raise Exception('Something went wrong!')


