import sqlite3, os

class v1_00_Context_Database(object):
    db_name = None
    db_conn = None
    db_cursor = None
    controller = None

    def __init__(self,
                 controller=None,
                 server_name='localhost',
                 port_number=5000
    ):
        if controller == None:
            raise Exception('Controller cannot be none!')

        self.controller = controller

        self.db_name = 'datavolume/{0}-{1}.db'\
                             .format(server_name, port_number)

        self.db_conn = None
        self.db_cursor = None

        self.validate_activities_table()


    def db_exec(self, sql_statement=None, sql_parameters=()):
        if sql_statement == None:
            return None

        _returned = None

        try:
            if self.db_cursor == None:
                raise Exception('Cursor does not exist!')
            self.db_cursor.execute(sql_statement, sql_parameters)
        except sqlite3.OperationalError as oe:
            raise
        except Exception as e:
            raise


    def close_db(self):
        if not self.db_cursor == None:
            self.db_cursor.close()
        if not self.db_conn == None:
            self.db_conn.close()
        self.db_cursor = None
        self.db_conn = None


    def open_db(self):
        try:
            self.db_conn = sqlite3.connect(self.db_name)
            self.db_cursor = self.db_conn.cursor()
        except Exception as e:
            if not self.db_cursor == None:
                self.db_cursor.close()
            if not self.db_conn == None:
                self.db_conn.close()
            raise


    def validate_activities_table(self):
        _returned = None

        try:
            self.open_db()
            self.db_exec('select * from activities')
            self.db_conn.commit()
        except sqlite3.OperationalError as oe:
            self.db_cursor.execute(
                    'CREATE TABLE activities ( '+\
                    '  activity string primary key, '+\
                    '  description string not null,'+\
                    '  state integer'+\
                    ');'
                )
        except Exception as e:
            raise
        finally:
            self.close_db()

#
# Activities table
#

    def set_activity(
        self,
        activity=None,
        description=None,
        state=False
    ):
        if activity == None:
            return False

        if not type(state) == bool:
            raise ValueError('State must be True or False')

        if state:
            activity_state = 1
        else:
            activity_state = 0

        returned = None
        try:
            self.open_db()
            self.db_exec('insert or replace into activities '+\
                           ' (activity, description, state) '+\
                           ' values (?,?,?)',
                           (activity, description, state))
            self.db_conn.commit()

        except Exception as e:
            raise
        finally:
            self.close_db()

        return True


