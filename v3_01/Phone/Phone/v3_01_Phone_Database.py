from Phone.v3_00_Phone_Database import v3_00_Phone_Database
import sqlite3, os

class v3_01_Phone_Database(v3_00_Phone_Database):

    def __init__(self,
                 controller=None,
                 server_name='localhost',
                 port_number=5000
    ):
        super(v3_01_Phone_Database, self).__init__(controller,
                                                   server_name,
                                                   port_number)

    def update_notification(
        self,
        sender=None,
        date_string=None,
        notification=None,
        action=None
    ):
        returned = None
        try:
            self.open_db()
            self.db_exec('update notifications '+\
                           'set notification_read = 1 '+\
                           'where sender = ? '+\
                           'and date_string = ? '+\
                           'and notification = ? '+\
                           'and action = ?',
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
                           'where notification_read = 0 '+\
                           'order by date_string')
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
        except sqlite3.OperationalError as soe:
            raise
        except Exception as e:
            raise

