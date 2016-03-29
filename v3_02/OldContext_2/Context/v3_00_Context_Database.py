import sqlite3, os

class v3_00_Context_Database(object):
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

        self.db_name = 'datavolume/{0}-{1}-Context.db'\
                             .format(server_name, port_number)

        self.db_conn = None
        self.db_cursor = None

        self.validate_notification_table()


    def get_bluetooth_device(self):
        return self.controller.get_value('bluetooth')


    def set_bluetooth_device(self, devicename):
        return self.controller.set_value('bluetooth', devicename)


    def save_notification(
        self,
        sender=None,
        date_string=None,
        notification=None,
        action=None
    ):
        returned = None
        try:
            self.open_db()
            self.db_exec('insert into notifications '+\
                           ' (sender, date_string, notification, '+\
                           'action, notification_read) '+\
                           ' values (?,?,?,?, 0)',
                           (sender, date_string, notification, action))
            self.db_conn.commit()

        except Exception as e:
            raise
        finally:
            self.close_db()

        return True


    def get_notifications(
        self
    ):
        returned = []
        try:
            self.open_db()
            self.db_exec('select sender, date_string, notification, '+\
                           'action '+\
                           'from notifications '+\
                           'where notification_read = 0')
            returned = self.db_cursor.fetchall()
        except Exception as e:
            raise
        finally:
            self.close_db()

        return returned


    def db_exec(self, sql_statement=None, sql_parameters=()):
        if sql_statement == None:
            return None

        _returned = None

        try:
            if self.db_cursor == None:
                raise Exception('Cursor does not exist!')
            self.db_cursor.execute(sql_statement, sql_parameters)
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


    def validate_notification_table(self):
        _returned = None

        try:
            self.open_db()
            self.db_exec('select * from notifications')
            self.db_exec('delete from notifications '+\
                           'where notification_read != 0'
                          )
            self.db_conn.commit()
        except sqlite3.OperationalError as oe:
            self.db_cursor.execute(
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
            self.close_db()

