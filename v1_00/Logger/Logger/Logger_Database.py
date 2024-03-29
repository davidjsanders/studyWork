import sqlite3
from datetime import datetime

class Logger_Database(object):
    __db_name = None
    __db_conn = None
    __db_cursor = None

    def __init__(self, server_name=None, port_number=None):
        if server_name == None:
            server = 'localhost'
        else:
            server = server_name
        if port_number == None:
            port_number = '5000'
        else:
            port_number = str(port_number)

        self.__db_name = 'datavolume/central-log-'+server+'-'+\
            port_number+'.db'
        self.__db_conn = None
        self.__db_cursor = None

        self.__validate_logging_table()


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


    def __validate_logging_table(self):
        _returned = None

        try:
            self.__open_db()
            self.__db_exec('delete from log')
            self.__db_conn.commit()
        except sqlite3.OperationalError as oe:
            print(str(oe))
            self.__db_cursor.execute(
                    'CREATE TABLE log( '+\
                    '  sender string not null,'
                    '  timestamp string not null, '+\
                    '  log_type string, '+\
                    '  message string, '+\
                    ' PRIMARY KEY(sender, timestamp)'+\
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


    def write_log(
        self,
        sender='unknown',
        log_type=None,
        message=None,
        timestamp=str(datetime.now())
    ):
        returned = False
        try:
            self.__open_db()
            self.__db_exec('insert or replace into log '+\
                           'values (?, ?, ?, ?)',
                           (sender,
                            timestamp, 
                            log_type, 
                            message)
                          )
            self.__db_conn.commit()
            returned = True
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()
            return returned


    def get_log(self):
        try:
            self.__open_db()
            self.__db_exec('select * from log')
            returned = self.__db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()
            if returned == []:
                returned = None

        return returned


    def get_log_by_sender(self, sender=None):
        try:
            self.__open_db()
            self.__db_exec('select * from log '+\
                           'where sender = ?',
                           (sender,)
                          )
            returned = self.__db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()
            if returned == []:
                returned = None

        return returned


    def get_log_by_timerange(self, time_start=None, time_end=None):
        try:
            self.__open_db()
            self.__db_exec('select * from log '+\
                           'where timestamp >= ? '+\
                           'and timestamp <= time_end ',
                           (time_start, time_end)
                          )
            returned = self.__db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()
            if returned == []:
                returned = None

        return returned


    def clear_log(
        self
    ):
        returned = False
        try:
            self.__open_db()
            self.__db_exec('delete from log')
            self.__db_conn.commit()
            returned = True
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()

        return returned

