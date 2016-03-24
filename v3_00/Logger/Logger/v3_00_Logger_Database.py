import sqlite3
from datetime import datetime
import time

class v3_00_Logger_Database(object):
    db_name = None
    db_conn = None
    db_cursor = None

    def __init__(self, server_name=None, port_number=None):
        if server_name == None:
            server = 'localhost'
        else:
            server = server_name
        if port_number == None:
            port_number = '5000'
        else:
            port_number = str(port_number)

        self.db_name = 'datavolume/central-log-'+server+'-'+\
            port_number+'.db'
        self.db_conn = None
        self.db_cursor = None

        self.validate_logging_table()


    def open_db(self):
        try:
            self.db_conn = sqlite3.connect(self.db_name)
            self.db_cursor = self.db_conn.cursor()
        except Exception as e:
            print(repr(e))
            if not self.db_cursor == None:
                self.db_cursor.close()
            if not self.db_conn == None:
                self.db_conn.close()


    def validate_logging_table(self):
        _returned = None

        try:
            self.open_db()
            self.db_exec('delete from log')
            self.db_conn.commit()
        except sqlite3.OperationalError as oe:
            print(str(oe))
            self.db_cursor.execute(
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
            self.close_db()


    def db_exec(self, sql_statement=None, sql_parameters=()):
        if sql_statement == None:
            return None

        _returned = None

        try:
            if self.db_cursor == None:
                raise Exception('Cursor does not exist!')
            self.db_cursor.execute(sql_statement, sql_parameters)
        except sqlite3.OperationalError as soe:
            raise
        except Exception as e:
            print(repr(e))
            raise


    def close_db(self):
        if not self.db_cursor == None:
            self.db_cursor.close()
        if not self.db_conn == None:
            self.db_conn.close()
        self.db_cursor = None
        self.db_conn = None


    def write_log(
        self,
        sender='unknown',
        log_type=None,
        message=None,
        timestamp=str(datetime.now())
    ):
        returned = False
        try:
            self.open_db()
            self.db_exec('insert or replace into log '+\
                           'values (?, ?, ?, ?)',
                           (sender,
                            timestamp, 
                            log_type, 
                            message)
                          )
            self.db_conn.commit()
            returned = True
        except Exception as e:
            print(repr(e))
        finally:
            self.close_db()
            return returned


    def get_log(self):
        try:
            self.open_db()
        except Exception as e:
            print('Get log caused exception: {0}'.format(repr(e)))
            raise

        try:
            self.db_exec('select * from log')
            returned = self.db_cursor.fetchall()
            retry_count = 6
        except sqlite3.OperationalError as oe:
            raise
        except Exception as e:
            raise Exception('Get log caused exception: {0}'.format(repr(e)))

        try:
            self.close_db()
        except Exception as e:
            print('Get log caused exception: {0}'.format(repr(e)))
            raise

        if returned == []:
            returned = None
        elif retry_count < 6:
            raise sqlite3.OperationalError('Database too busy.')

        return returned


    def get_log_by_sender(self, sender=None):
        try:
            self.open_db()
            self.db_exec('select * from log '+\
                           'where sender = ?',
                           (sender,)
                          )
            returned = self.db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.close_db()
            if returned == []:
                returned = None

        return returned


    def get_log_by_timerange(self, time_start=None, time_end=None):
        try:
            self.open_db()
            self.db_exec('select * from log '+\
                           'where timestamp >= ? '+\
                           'and timestamp <= time_end ',
                           (time_start, time_end)
                          )
            returned = self.db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.close_db()
            if returned == []:
                returned = None

        return returned


    def clear_log(
        self
    ):
        returned = False
        try:
            self.open_db()
            self.db_exec('delete from log')
            self.db_conn.commit()
            returned = True
        except Exception as e:
            print(repr(e))
        finally:
            self.close_db()

        return returned

