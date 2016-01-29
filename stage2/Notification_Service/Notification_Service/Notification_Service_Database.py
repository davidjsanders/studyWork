import sqlite3

class Notification_Service_Database(object):
    __db_name = None
    __db_conn = None
    __db_cursor = None

    def __init__(self):
        self.__db_name = 'datavolume/Notification_Service.db'
        self.__db_conn = None
        self.__db_cursor = None

        self.__validate_config_table()
        self.__validate_notification_table()


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
            self.__db_exec('insert or replace into config values (?,?)',
                          ('Notification_Service','ABCD-EFGH'))
            self.__db_exec('insert or replace into config values (?,?)',
                          ('locked','unlocked'))
            self.__db_conn.commit()
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


    def get_bluetooth_device(self):
        returned = None
        try:
            self.__open_db()
            self.__db_exec('select value from config where key = ?',
                           ('bluetooth',))
            returned = self.__db_cursor.fetchall()
            if not returned == []:
                if type(returned) == list:
                    returned = returned[0][0]
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()

        return returned


    def set_bluetooth_device(self, devicename):
        returned = None
        try:
            self.__open_db()
            self.__db_exec('insert into config values (?,?)',
                          ('bluetooth', devicename))
            self.__db_conn.commit()
            self.__db_exec('select value from config '+\
                           'where key = ? and value = ?',
                           ('bluetooth', devicename))
            returned = self.__db_cursor.fetchall()
            if not returned == []:
                if type(returned) == list:
                    returned = returned[0][0]
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()

        return returned


    def check_pairing(self, devicename):
        returned = None
        try:
            self.__open_db()
            self.__db_exec('select key from paired_devices where device = ?',
                           (devicename,))
            returned = self.__db_cursor.fetchall()
            if not returned == []:
                if type(returned) == list:
                    returned = returned[0][0]

        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()

        return returned

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


    def pair_device(self, devicename):
        try:
            pairing_key = '1234-5678-9012-3456'

            self.__open_db()
            self.__db_exec('insert or replace into '+\
                           'paired_devices values (?, ?)',
                           (devicename, pairing_key))
            self.__db_conn.commit()
        except:
            raise
        finally:
            self.__close_db()

        return pairing_key

    def remove_pairing(self, devicename):
        try:
            self.__open_db()
            self.__db_exec('delete from paired_devices where device = ?',
                           (devicename,))
            self.__db_conn.commit()
        except:
            raise
        finally:
            self.__close_db()

        return True
