import sqlite3, os

class Phone_Database(object):
    __db_name = None
    __db_conn = None
    __db_cursor = None
    __controller = None

    def __init__(self,
                 controller=None,
                 server_name='localhost',
                 port_number=5000
    ):
        if controller == None:
            raise Exception('Controller cannot be none!')

        self.__controller = controller

        self.__db_name = 'datavolume/{0}-{1}-phone.db'\
                             .format(server_name, port_number)

        self.__db_conn = None
        self.__db_cursor = None

        self.__validate_notification_table()


    def get_bluetooth_device(self):
        return self.__controller.get_value('bluetooth')


    def set_bluetooth_device(self, devicename):
        return self.__controller.set_value('bluetooth', devicename)


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
            raise
        finally:
            self.__close_db()

        return True


    def get_notifications(
        self
    ):
        returned = []
        try:
            self.__open_db()
            self.__db_exec('select sender, date_string, notification, '+\
                           'action '+\
                           'from notifications '+\
                           'where notification_read = 0')
            returned = self.__db_cursor.fetchall()
        except Exception as e:
            raise
        finally:
            self.__close_db()

        return returned


    def __db_exec(self, sql_statement=None, sql_parameters=()):
        if sql_statement == None:
            return None

        _returned = None

        try:
            if self.__db_cursor == None:
                raise Exception('Cursor does not exist!')
            self.__db_cursor.execute(sql_statement, sql_parameters)
        except Exception as e:
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
            if not self.__db_cursor == None:
                self.__db_cursor.close()
            if not self.__db_conn == None:
                self.__db_conn.close()
            raise


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
            raise
        finally:
            self.__close_db()

