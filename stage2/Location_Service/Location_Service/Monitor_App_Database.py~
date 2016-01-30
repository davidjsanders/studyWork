import sqlite3

class Monitor_App_Database(object):
    __db_name = None
    __db_conn = None
    __db_cursor = None

    def __init__(self):
        self.__db_name = 'datavolume/Monitor_App.db'
        self.__db_conn = None
        self.__db_cursor = None

        self.__validate_config_table()
        self.set_state(state='off')


    def __open_db(self):
        try:
            self.__db_conn = sqlite3.connect(self.__db_name)
            self.__db_cursor = self.__db_conn.cursor()
        except Exception as e:
            print(repr(e))
            if not self.__db_cursor == None:
                self.__db_cursor.close()
            if not self.__db_conn == None:
                self.__db_conn.close()


    def __validate_config_table(self):
        _returned = None

        try:
            self.__open_db()
            self.__db_exec('select * from config')
            self.__db_exec('delete from config')
            self.__db_conn.commit()
        except sqlite3.OperationalError as oe:
            print(str(oe))
            self.__db_cursor.execute(
                    'CREATE TABLE config( '+\
                    '  key string primary key, '+\
                    '  value string '+\
                    ')'
                )
        except Exception as e:
            print(repr(e))
            raise
        finally:
            self.__close_db()


    def __db_exec(self, sql_statement=None, sql_parameters=()):
        if sql_statement == None:
            return None

        _returned = None

        try:
            if self.__db_cursor == None:
                raise Exception('Cursor does not exist!')
            self.__db_cursor.execute(sql_statement, sql_parameters)
        except Exception as e:
            print(repr(e))
            raise


    def __close_db(self):
        if not self.__db_cursor == None:
            self.__db_cursor.close()
        if not self.__db_conn == None:
            self.__db_conn.close()
        self.__db_cursor = None
        self.__db_conn = None


    def set_state(self, state=None):
        return self.set_value(key='state', value=state)
        

    def get_state(self):
        return self.get_value(key='state')


    def set_value(self, key=None, value=None):
        returned = []
        try:
            self.__open_db()
            self.__db_exec('insert or replace into config '+\
                           'values (?, ?)',
                           (key, value)
                          )
            self.__db_conn.commit()
            returned = self.get_value(key=key)
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()
            return returned


    def get_value(self, key=None):
        try:
            if key == None:
                return []

            self.__open_db()
            self.__db_exec('select value from config '+\
                           'where key = ?',
                           (key,))
            returned = self.__db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()
            if type(returned) == list \
            and returned != []:
                returned = returned[0][0]
            else:
                returned = None

        return returned


