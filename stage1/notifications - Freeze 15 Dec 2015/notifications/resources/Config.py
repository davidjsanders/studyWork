from notifications import app, api
import sqlite3

port_number = 5000
server_name = 'localhost'

controlkey_master = 'ABC123'
__schema_filename__ = 'schemas/notification.json'
__pair_schema_filename__ = 'schemas/pair.json'

def initialize():
    database_okay = False
    db = db_get()

    try:
        get_key('android')
        database_okay=True
    except sqlite3.OperationalError as sqlOE:
        print("Warning: Configuration table doesn't exist. It will be created.")
    except Exception:
        raise

    if not database_okay:
        db_execute(
            database=db,
            sql_statement='create table configuration '+
                          '(key string primary key, value string)'
        )
        db_execute(
            database=db,
            sql_statement='insert into configuration values (?, ?)',
            args=('android','FALSE')
        )
        db_execute(
            database=db,
            sql_statement='insert into configuration values (?, ?)',
            args=('pre-lollipop','FALSE')
        )
        db_execute(
            database=db,
            sql_statement='insert into configuration values (?, ?)',
            args=('locked','TRUE')
        )
        db_execute(
            database=db,
            sql_statement='insert into configuration values (?, ?)',
            args=('bluetooth',None)
        )
        db.commit()

    database_okay = False
    try:
        db_execute(
            database=db,
            sql_statement='select * from notifications'
        )
        database_okay = True
    except sqlite3.OperationalError as sqlOE:
        print("Warning: Notifications table doesn't exist. It will be created.")
    except Exception:
        raise

    if not database_okay:
        db_execute(
            database=db,
            sql_statement='create table notifications '+
                          '(key number primary key, value string)'
        )


def db_close(database=None):
    try:
        if database is not None:
            database.close()
    except Exception:
        raise

def db_get():
    try:
        database_name = get_database()
        database = sqlite3.connect(database_name)

        if database == None:
            raise Exception('Unable to connect to database.')

        return database
    except Exception:
        raise

def db_execute(database=None, sql_statement=None, args=(), multiple=False):
    if sql_statement == None:
        return []

    if database == None:
        database = db_get()

    return_data = database.execute(sql_statement, args)\
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

    database = db_get()
    try:
        db_key = db_execute(
            database=database,
            sql_statement='select value from configuration where key = ?',
            args=(key,)
        )
        db_close(database)
        if db_key == [] or db_key[0] == '':
            return None # Default to a locked state if database is empty!

        return db_key[0]
    except Exception as e:
        raise

def set_key(key=None, value=None):
    if key==None or value==None:
        return False

    database = db_get()
    try:
        db_key = db_execute(
            database=database,
            sql_statement='insert or replace into configuration '+\
                          '(key, value) values (?, ?)',
            args=(key, value)
        )
        database.commit()
        database.close()
        return get_key(key)
    except Exception as e:
        raise

def delete_key(key=None):
    if key==None:
        return False

    database = db_get()
    try:
        db_key = db_execute(
            database=database,
            sql_statement='delete from configuration '+\
                          'where key = ?',
            args=(key,)
        )
        database.commit()
        database.close()
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

        if db_records.upper() == 'TRUE':
            return True;
        else:
            return False;
    except Exception as e:
        raise Exception('Something went wrong!'+repr(e))


