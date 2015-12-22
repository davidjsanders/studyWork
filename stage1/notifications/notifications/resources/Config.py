"""
    module: Config.py
    ------------------------------------------------------------------------
    Author:      David J. Sanders
    Student No:  H00035340
    Last Update: 22 December 2015
    Update:      Add device_locked sentinel
                 Revise documentation
    ------------------------------------------------------------------------
    Overivew:    Config package contains the 'library' of common routines and
                 settings.

    Purpose:     Provides the configuration resources and common routines used
                 within the application. NB; when using uWSGI, setting global
                 variables and updating them through Config is NOT thread safe
                 and will cause inconsistent behaviours.

    References
    ----------

"""
#Import the app and api contexts
from notifications import app, api

#import the SQLite3 package to connect to the database
import sqlite3

DEVICE_LOCKED_SENTINEL = \
    'DEVICE_LOCKED!'         # Used as a constant

port_number = 5000           # Default port number if not provided
server_name = 'localhost'    # Default server name if not provided

controlkey_master = 'ABC123' # Control key to emulate secure communications
                             # between services

unlock_code = 1234           # Simple code to emulate device lock/unlock

# Schema Files
__schema_filename__ = 'schemas/notification.json'  # Notification schema
__pair_schema_filename__ = 'schemas/pair.json'     # Pairing shcema

#
# Initialize(). Called from runserver.py to validate database is okay. If it
# is not, then the database and tables get created and populated.
#
def initialize():
    database_okay = False    # Sentinel for database checking
    db = db_get()            # Call db_get and get a database instance

    # Check if the configuration table exists
    try:
        get_key('android')   # Get the key 'android' from the configuration
                             # table. If it raises an exception, then it does
                             # not exist.

        database_okay=True   # If we made it here, then all is good.
    except sqlite3.OperationalError as sqlOE:
        # configuration table doesn't exist. Log it and move on.
        print("Warning: Configuration table doesn't exist. It will be created.")
    except Exception:
        raise    # Catch any other exceptions.

    # If the configuration table didn't exist, create and populate it
    if not database_okay:
        # Call standard database module to create configuration table
        db_execute(
            database=db,
            sql_statement='create table configuration '+
                          '(key string primary key, value string)'
        )

        # Call standard database module to populate configuration table
        # Populate android key - default to FALSE
        db_execute(
            database=db,
            sql_statement='insert into configuration values (?, ?)',
            args=('android','FALSE')
        )
        # Populate pre-lollipop key - default to FALSE
        db_execute(
            database=db,
            sql_statement='insert into configuration values (?, ?)',
            args=('pre-lollipop','FALSE')
        )
        # Populate locked key - default to TRUE
        db_execute(
            database=db,
            sql_statement='insert into configuration values (?, ?)',
            args=('locked','TRUE')
        )
        # Populate Bluetooth pair key - default to None
        db_execute(
            database=db,
            sql_statement='insert into configuration values (?, ?)',
            args=('bluetooth',None)
        )
        # Commit the inserts
        db.commit()

    # Reset the sentinel and check the notifications table exists
    database_okay = False
    try:
        db_execute(
            database=db,
            sql_statement='select * from notifications'
        )
        database_okay = True    # If we got here, then notifications exists
    except sqlite3.OperationalError as sqlOE:
        print("Warning: Notifications table doesn't exist. It will be created.")
    except Exception:
        raise    # Catch any other exceptions

    # If the configuration table didn't exist, create and populate it
    if not database_okay:
        # Create the notifications table but DO NOT populate it
        db_execute(
            database=db,
            sql_statement='create table notifications '+
                          '(key number primary key, value string)'
        )


def db_close(database=None):
    '''
db_close(database=<sqlite3_database_connection>)
Check if a connection is open. If it is, close it
    '''
    try:
        if database is not None:
            database.close()
    except Exception:
        raise

def db_get():
    '''
db_get()
Open a connection to the database
    '''
    try:
        # get the database file name
        database_name = get_database()

        # open a connection to it
        database = sqlite3.connect(database_name)

        # If no db object was returned, raise an exception
        if database == None:
            raise Exception('Unable to connect to database.')

        # otherwise, return the db object
        return database
    except Exception:
        raise

def db_execute(database=None, sql_statement=None, args=(), multiple=False):
    '''
db_execute(database=<sqlite3_database_connection>,
           sql_statement='select lorem from ipsum where dolor = ?',
           args=(arg1, ),
           multiple=True|False)
Check database connection is open (if not, get one) and then execute a single
or multi-row statement against the database.
    '''
    # Check the SQL is not None. NB, there is no SQL syntax or semantic check
    if sql_statement == None:
        return []

    # Check the database is already open
    if database == None:
        # If not, open it
        database = db_get()

    # Execute the sql statement passing args to avoid SQL Injection
    return_data = database.execute(sql_statement, args)\
                      .fetchall()

    # If only expecting a single row from the DB
    if not multiple:
        # Check that something was returned
        if not return_data == []:
            return_data = return_data[0]    # Only return first row

    return return_data    # return results

def get_database():
    '''
get_database()
Return the name of the database based on the server_name and port_number. For
example, the app running on machineX on port 89 would have a database name of
notifications-machineX-89.db in a folder called datavol/
    '''
    return 'datavol/notifications-'+\
           str(server_name)+'-'+\
           str(port_number)+\
           '.db'

def set_contexts():
    '''
set_contexts()
Enables the setting of certain configuration key/value pairs into a schema which
can then be used to restrict the information dumped (serialized) by the 
marshmallow package.
    '''

    # Create a temporary dictionary to hold the results
    new_schema = {}
    if check_key('android'):           # Check if the model is Android based
        new_schema['android'] = True
    if check_key('locked'):            # Check if the model is locked
        new_schema['locked'] = True
    if check_key('pre-lollipop'):      # Check if pre-lollipop Android is set
        new_schema['pre-lollipop'] = True

    # Return the temporary dictionary as the 
    return new_schema

def check_prelollipop(schema=None):
    '''
check_prelollipop(schema=the_schema)
Checks to see if 'prelollipop' has been set in a schema. If it has, an exception
is raised if the device is locked AND it IS a prelollipop device
    '''
    # Ignore if schema is empty
    if schema == None:
        return

    if 'pre-lollipop' in schema \
    and 'locked' in schema:
        raise RuntimeError('Device is locked.')

def get_key(key=None):
    '''
get_key(key='the_key')
Query the database and return the value for a given key/value pair.
    '''
    # If the key is empty, return None
    if key==None:
        return None

    # Open the database
    database = db_get()
    try:
        # get the value for the given key.
        db_key = db_execute(
            database=database,
            sql_statement='select value from configuration where key = ?',
            args=(key,)
        )
        db_close(database)

        # If nothing is returned, return None
        if db_key == [] or db_key[0] == '':
            return None # Default to a locked state if database is empty!

        # Return the value retrieved from the database. NOTE: If more than one
        # row is returned (this should never happen as KEY is a primary key),
        # then only the first row will be returned.
        return db_key[0]
    except Exception as e:
        raise

def set_key(key=None, value=None):
    '''
set_key(key='the_key', value='The Value')
Set the value of a key value pair. If the key doesn't exist, it is created; if 
it exists, it is updated.
    '''
    # An empty key cannot be set
    if key==None or value==None:
        return None

    # Open the database
    database = db_get()
    try:
        # Insert (OR REPLACE) the key/value pair
        db_key = db_execute(
            database=database,
            sql_statement='insert or replace into configuration '+\
                          '(key, value) values (?, ?)',
            args=(key, value)
        )
        # Commit the transaction
        database.commit()

        # Close the database
        database.close()

        # return the value
        return value
    except Exception as e:
        raise

def delete_key(key=None):
    '''
delete_key(key='the_key')
Delete a key value pair. If the key doesn't exist, it is reported back as a
successful deletion.
    '''
    # An empty key cannot be deleted
    if key==None:
        return False

    # Open the database
    database = db_get()
    try:
        # Delete the k/v pair
        db_key = db_execute(
            database=database,
            sql_statement='delete from configuration '+\
                          'where key = ?',
            args=(key,)
        )
        # Commit the transaction
        database.commit()

        # Close the DB
        database.close()

        # Return true for success
        return True
    except Exception as e:
        raise

def check_key(key=None):
    '''
check_key(key='the_key')
Check a key/value pair and return true if it is set to TRUE.
    '''
    # An empty key cannot be checked
    if key==None:
        return False

    try:
        # Get the key's value
        db_records = get_key(key)

        # If it doesn't exist (i.e. we got no results) default to True
        if db_records == None:
            return True 

        # If it contains the string (NB NOT a bool) 'TRUE'
        if db_records.upper() == 'TRUE':
            return True;
        else:
            return False;
    except Exception as e:
        raise

