import sqlite3

class Pairing_Database(object):

    __db_name = 'datavolume/pairing.db'
    __db_conn = None
    __db_cursor = None

    def __init__(self):
        self.__db_name = 'datavolume/pairing.db'
        self.__db_conn = None
        self.__db_cursor = None

        self.__validate_pairing_table()


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


    def __validate_pairing_table(self):
        _returned = None

        try:
            self.__open_db()
            self.__db_exec('select * from paired_devices')
        except sqlite3.OperationalError as oe:
            self.__db_cursor.execute(
                    'create table paired_devices '+\
                    '(device string, key string)'
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
