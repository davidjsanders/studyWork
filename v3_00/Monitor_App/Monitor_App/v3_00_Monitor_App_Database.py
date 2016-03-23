import sqlite3, os

class v3_00_Monitor_App_Database(object):
    db_name = None
    db_conn = None
    db_cursor = None
    server_name = None
    port_number = None
    controller = None

    def __init__(self, controller=None,
                       port_number='5000',
                       server_name='localhsot'):
        if controller == None:
            raise Exception('Controller cannot be none.')

        self.controller = controller

        self.server_name = server_name
        self.port_number = port_number

        self.db_name = 'datavolume/'+server_name+'-'+\
            str(port_number)+'-monitor.db'
        self.db_conn = None
        self.db_cursor = None

        self.validate_app_table()
        self.set_state(state='off')


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


    def validate_app_table(self):
        _returned = None

        try:
            self.open_db()
            self.db_exec('delete from apps')
            self.db_conn.commit()
        except sqlite3.OperationalError as oe:
            print(str(oe))
            self.db_cursor.execute(
                    'CREATE TABLE apps( '+\
                    '  app string primary key, '+\
                    '  description string '+\
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


    def set_state(self, state=None):
        return self.controller.set_value(key='state', value=state)
        

    def get_state(self):
        return self.controller.get_value(key='state')


    def get_app(self, application=None):
        try:
            if application == None:
                return []

            self.open_db()
            self.db_exec('select upper(app), description '+\
                           'from apps '+\
                           'where upper(app) = ?',
                           (application.upper(),))
            returned = self.db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.close_db()

        return returned


    def get_apps(self):
        try:
            self.open_db()
            self.db_exec('select upper(app), description from apps')
            returned = self.db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.close_db()

        return returned


    def set_app(self, application=None, description=None):
        returned = []
        try:
            self.open_db()
            self.db_exec('insert or replace into apps '+\
                           'values (?, ?)',
                           (application.upper(), description)
                          )
            self.db_conn.commit()
            returned = self.get_app(application=application)
        except Exception as e:
            print(repr(e))
        finally:
            self.close_db()

        return returned


    def delete_app(self, application=None):
        returned = False
        try:
            self.open_db()
            self.db_exec('delete from apps '+\
                           'where upper(app) = ?',
                           (application.upper(),)
                          )
            self.db_conn.commit()
            returned = True
        except Exception as e:
            print(repr(e))
        finally:
            self.close_db()

        return returned

