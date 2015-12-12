from notifications import app, api
import sqlite3

port_number = 5000
server_name = 'localhost'

controlkey_master = 'ABC123'
__schema_filename__ = 'schemas/notification.json'
__pair_schema_filename__ = 'schemas/pair.json'

def db_close():
    database = getattr(app.app_context().g, '_database', None)
    if database is not None:
        database.close()

def db_get():
    database = None
    database = getattr(app.app_context().g, '_database', None)

    if database == None:
        database_name = get_database()
        database = app.app_context().g._database = sqlite3.connect(database_name)

    if database == None:
        raise Exception('Unable to connect to database.')

    return database

def db_execute(sql_statement=None, args=(), multiple=False):
    if sql_statement == None:
        return []

    return_data = db_get().execute(sql_statement, args)\
                      .fetchall()

    if not multiple:
        if not return_data == []:
            return_data = return_data[0]

    return return_data

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

    db_get()
    try:
        db_key = db_execute(
            sql_statement='select value from configuration where key = ?',
            args=(key,)
        )
        db_close()
        if db_key == [] or db_key[0] == '':
            return None # Default to a locked state if database is empty!

        return db_key[0]
    except Exception as e:
        raise

def set_key(key=None, value=None):
    print('Set 1')
    if key==None or value==None:
        return False

    print('Set 2')
    try:
        db_key = db_execute(
            sql_statement='insert or replace into configuration '+\
                          '(key, value) values (?, ?)',
            args=(key, value)
        )
        db_get().commit()
        db_close()
        return get_key(key)
    except Exception as e:
        raise

def delete_key(key=None):
    if key==None:
        return False

    database_name = 'datavol/notifications.db'
    try:
        db_key = db_execute(
            sql_statement='delete from configuration '+\
                          'where key = ?',
            args=(key,)
        )
        db_get().commit()
        db_close()
        return True
    except Exception as e:
        raise

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


