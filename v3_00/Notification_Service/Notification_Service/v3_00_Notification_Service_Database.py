import sqlite3, os

class v3_00_Notification_Service_Database(object):
    db_name = None
    db_conn = None
    db_cursor = None

    def __init__(self,
                 port_number='5000',
                 server_name='localhost'
    ):
        self.server_name = server_name
        self.port_number = port_number

        self.db_name = 'datavolume/'+server_name+'-'+str(port_number)+\
            '-notifications.db'

        self.db_conn = None
        self.db_cursor = None

        self.validate_notification_table()


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


    def validate_notification_table(self):
        _returned = None

        try:
            self.open_db()
            self.db_exec('select * from notifications')
        except sqlite3.OperationalError as oe:
            print(str(oe))
            self.db_cursor.execute(
                    'CREATE TABLE notifications( '+\
                    '  id integer primary key autoincrement, '+\
                    '  sender string not null, '+\
                    '  recipient string not null,' +\
                    '  notification string not null, '+\
                    '  action string not null, '+\
                    '  event_date string not null '+\
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
        except sqlite3.OperationalError as oe:
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


    def get_notifications(
        self,
        recipient=None
    ):
        if recipient == None:
            return []

        returned = None
        try:
            self.open_db()
            self.db_exec('select * from notifications '+\
                           'where recipient = ?',
                           (recipient,))
            returned = self.db_cursor.fetchall()
            self.db_conn.commit()
        except Exception as e:
            print(repr(e))
        finally:
            self.close_db()

        return returned


    def clear_notification(
        self,
        identifier=None
    ):
        if identifier == None:
            return []

        returned = True
        try:
            self.open_db()
            self.db_exec('delete from notifications '+\
                           'where id = ?',
                           (identifier,))
            self.db_conn.commit()
        except Exception as e:
            returned = False
            print(repr(e))
        finally:
            self.close_db()

        return returned


    def clear_notifications(
        self,
        recipient=None
    ):
        if recipient == None:
            return []

        returned = True
        try:
            self.open_db()
            self.db_exec('delete from notifications '+\
                           'where recipient = ?',
                           (recipient,))
            self.db_conn.commit()
        except Exception as e:
            returned = False
            print(repr(e))
        finally:
            self.close_db()

        return returned


    def save_notification(
        self,
        sender=None,
        recipient=None,
        text=None,
        action=None,
        event_date=None
    ):
        returned = None
        try:
            self.open_db()
            self.db_exec('insert into notifications ('+\
                           ' sender, '+\
                           ' recipient, '+\
                           ' notification, '+\
                           ' action, '+\
                           ' event_date) '+\
                           'values (?,?,?,?,?)',
                           (sender, recipient, text, action, event_date))
            self.db_conn.commit()
        except Exception as e:
            print(repr(e))
        finally:
            self.close_db()

        return True


