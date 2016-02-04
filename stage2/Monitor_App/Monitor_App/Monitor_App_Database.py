import sqlite3, os

class Monitor_App_Database(object):
    __db_name = None
    __db_conn = None
    __db_cursor = None
    __server_name = None
    __port_number = None

    def __init__(self):
        stage = 0
        try:
            stage += 1
            port_number = os.environ['portToUse']
            stage += 1
            server_name = os.environ['serverName']
        except KeyError as ke:
            if stage == 1:
                port_number = 5000
                server_name = 'localhost'
            else:
                server_name = 'localhost'

        self.__server_name = server_name
        self.__port_number = port_number

        self.__db_name = 'datavolume/'+server_name+'-'+\
            str(port_number)+'-monitor.db'
        self.__db_conn = None
        self.__db_cursor = None

        self.__validate_config_table()
        self.__validate_app_table()
        self.set_state(state='off')


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


    def __validate_app_table(self):
        _returned = None

        try:
            self.__open_db()
            self.__db_exec('select * from apps')
            self.__db_conn.commit()
        except sqlite3.OperationalError as oe:
            print(str(oe))
            self.__db_cursor.execute(
                    'CREATE TABLE apps( '+\
                    '  app string primary key, '+\
                    '  description string '+\
                    ')'
                )
        except Exception as e:
            print(repr(e))
            raise
        finally:
            self.__close_db()


    def __validate_config_table(self):
        _returned = None

        try:
            self.__open_db()
            self.__db_exec('select * from config')
            self.__db_exec('delete from config')
            self.__db_conn.commit()
        except sqlite3.OperationalError as oe:
            print(str(oe))
            self.__db_cursor.execute(
                    'CREATE TABLE config( '+\
                    '  key string primary key, '+\
                    '  value string '+\
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


    def set_state(self, state=None):
        return self.set_value(key='state', value=state)
        

    def get_state(self):
        return self.get_value(key='state')


    def get_app(self, application=None):
        try:
            if application == None:
                return []

            self.__open_db()
            self.__db_exec('select upper(app), description '+\
                           'from apps '+\
                           'where upper(app) = ?',
                           (application.upper(),))
            returned = self.__db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()

        return returned


    def get_apps(self):
        try:
            self.__open_db()
            self.__db_exec('select upper(app), description from apps')
            returned = self.__db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()

        return returned


    def set_app(self, application=None, description=None):
        returned = []
        try:
            self.__open_db()
            self.__db_exec('insert or replace into apps '+\
                           'values (?, ?)',
                           (application.upper(), description)
                          )
            self.__db_conn.commit()
            returned = self.get_app(application=application)
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()

        return returned


    def delete_app(self, application=None):
        returned = False
        try:
            self.__open_db()
            self.__db_exec('delete from apps '+\
                           'where upper(app) = ?',
                           (application.upper(),)
                          )
            self.__db_conn.commit()
            returned = True
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()

        return returned


    def set_value(self, key=None, value=None):
        returned = []
        try:
            self.__open_db()
            self.__db_exec('insert or replace into config '+\
                           'values (?, ?)',
                           (key, value)
                          )
            self.__db_conn.commit()
            returned = self.get_value(key=key)
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()
            return returned


    def get_value(self, key=None):
        try:
            if key == None:
                return []

            self.__open_db()
            self.__db_exec('select value from config '+\
                           'where key = ?',
                           (key,))
            returned = self.__db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()
            if type(returned) == list \
            and returned != []:
                returned = returned[0][0]
            else:
                returned = None

        return returned


