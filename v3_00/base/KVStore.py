import sqlite3

class KVStore(object):
    __db_name = 'datavolume/pairing.db'
    __db_conn = None
    __db_cursor = None
#    __server_name = None
#    __port_number = None

    def __init__(self, db_name=None):
        if not db_name == None:
            self.__db_name = db_name

        self.__validate_config_table()


    def clear_key(self, key=None):
        if key == None:
            return None

        return_value = False
        try:
            self.__open_db()
            self.__db_exec('delete from config where key = ?',
                          (key,))
            self.__db_conn.commit()
            return_value = None
        except Exception as e:
            raise
        finally:
            self.__close_db()

        return return_value



    def set_key(self, key=None, value=None):
        if key == None:
            return None

        return_value = False
        try:
            self.__open_db()
            self.__db_exec('insert or replace into config values (?,?)',
                          (key,value))
            self.__db_conn.commit()
            return_value = value
        except Exception as e:
            raise
        finally:
            self.__close_db()

        return return_value


    def get_key(self, key=None):
        if key == None:
            return None

        returned = []
        try:
            self.__open_db()
            self.__db_exec('select value from config where key = ?',
                          (key,))
            returned = self.__db_cursor.fetchall()
            if returned != []:
                returned = returned[0][0] # Only return first value
            elif returned == []:
                returned = None
            return_value = returned
        except Exception as e:
            raise
        finally:
            self.__close_db()

        return return_value


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
            self.__db_exec('delete from config')
            self.__db_conn.commit()
        except sqlite3.OperationalError as oe:
            print('Initializing config table')
            self.__db_cursor.execute(
                    'create table config '+\
                    '(key string primary key not null, value string)'
                )
        except Exception as e:
#            print(repr(e))
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
        except sqlite3.OperationalError as oe:
            raise
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



