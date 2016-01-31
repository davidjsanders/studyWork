import sqlite3

class Phone_Database(object):
    __db_name = None
    __db_conn = None
    __db_cursor = None

    def __init__(self, server_name=None, port_number=None):
        if server_name != None and port_number != None:
            self.__db_name = 'datavolume/phone-'+\
                             server_name+'-'+str(port_number)+'.db'
            self.__db_conn = None
            self.__db_cursor = None

            self.__validate_config_table()
            self.__validate_notification_table()


    def clear_key(self, key=None):
        if key == None:
            return None

        return_value = False
        try:
            self.__open_db()
            self.__db_exec('delete from config where key = ?',
                          (key,))
            self.__db_conn.commit()
            return_value = True
        except Exception as e:
            print(repr(e))
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
            print(repr(e))
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
        except Exception as e:
            print(repr(e))
            raise
        finally:
            self.__close_db()

        return returned


    def get_bluetooth_device(self):
        return self.get_key('bluetooth')


    def set_bluetooth_device(self, devicename):
        return self.set_key('bluetooth', devicename)


    def save_notification(
        self,
        sender=None,
        date_string=None,
        notification=None,
        action=None
    ):
        returned = None
        try:
            self.__open_db()
            self.__db_exec('insert into notifications '+\
                           ' (sender, date_string, notification, '+\
                           'action, notification_read) '+\
                           ' values (?,?,?,?, 0)',
                           (sender, date_string, notification, action))
            self.__db_conn.commit()

        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()

        return True


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
        except sqlite3.OperationalError as oe:
            self.__db_cursor.execute(
                    'create table config '+\
                    '(key string primary key not null, value string)'
                )
        except Exception as e:
            print(repr(e))
            raise
        finally:
            self.set_key('phonename','noname')
            self.set_key('locked','unlocked')
            self.__close_db()


    def __validate_notification_table(self):
        _returned = None

        try:
            self.__open_db()
            self.__db_exec('select * from notifications')
            self.__db_exec('delete from notifications '+\
                           'where notification_read != 0'
                          )
            self.__db_conn.commit()
        except sqlite3.OperationalError as oe:
            self.__db_cursor.execute(
                    'CREATE TABLE notifications( '+\
                    '  id integer primary key autoincrement, '+\
                    '  sender string not null, '+\
                    '  date_string string not null, '+\
                    '  notification string not null, '+\
                    '  action string not null, '+\
                    '  notification_read int not null '+\
                    ');'
                )
        except Exception as e:
            print(repr(e))
            raise
        finally:
            self.__close_db()

