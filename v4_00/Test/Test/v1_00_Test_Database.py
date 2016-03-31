import sqlite3, os

class v1_00_Test_Database(object):
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

        self.validate_Test_table()


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


    def validate_Test_table(self):
        _returned = None

        try:
            self.open_db()
            self.db_exec('select * from module')
            self.db_conn.commit()
        except sqlite3.OperationalError as oe:
            self.db_cursor.execute(
                    'CREATE TABLE module ( '+\
                    '  id integer primary key autoincrement, '+\
                    '  some_field string not null '+\
                    ');'
                )
        except Exception as e:
            raise
        finally:
            self.close_db()

