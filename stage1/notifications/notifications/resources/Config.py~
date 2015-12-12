from notifications import app, api
import sqlite3

port_number = 5000
server_name = 'localhost'

controlkey_master = 'ABC123'
__schema_filename__ = 'schemas/notification.json'
__pair_schema_filename__ = 'schemas/pair.json'

def get_database():
    return 'datavol/notifications-'+\
           str(server_name)+'-'+\
           str(port_number)+\
           '.db'

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

def get_key(key=None):
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
            return None # Default to a locked state if database is empty!
        else:
            return db_records[0]

    except Exception as e:
        raise Exception('Something went wrong '+repr(e))

def set_key(key=None, value=None):
    if key==None or value==None:
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
            'insert or replace into configuration (key, value) values (?, ?)',
            (key, value) \
        )
        db_connection.commit()

        db_cursor.close()
        db_connection.close()

        return get_key(key)
    except Exception as e:
        raise Exception('Something went wrong!'+repr(e))

def delete_key(key=None):
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
            'delete from configuration where key = ?',
            (key,) \
        )
        db_connection.commit()

        db_cursor.close()
        db_connection.close()

        return True

    except Exception as e:
        raise Exception('Something went wrong!'+repr(e))

def check_key(key=None):
    if key==None:
        return False

    try:
        return_data = ''
        database_opened = False
        updated_data = False

        db_records = get_key(key)

        if db_records == None:
            return True # Default to a locked state if database is empty!

        if db_records[0].upper() == 'TRUE':
            return True;
        else:
            return False;
    except Exception as e:
        raise Exception('Something went wrong!'+repr(e))


