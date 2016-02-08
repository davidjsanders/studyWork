import sqlite3, os

class Pairing_Database(object):

    __db_name = 'datavolume/pairing.db'
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
            str(port_number)+'-pairing.db'
        self.__db_conn = None
        self.__db_cursor = None

        self.__validate_pairing_table()
        self.__validate_config_table()
        self.__validate_output_table()


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
            raise
        finally:
            self.__close_db()

        return returned


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
                    '(device string not null primary key, key string)'
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
        except sqlite3.OperationalError as oe:
            self.__db_cursor.execute(
                    'create table config '+\
                    '(key string primary key not null, value string)'
                )
        except Exception as e:
            print(repr(e))
            raise
        finally:
            self.__close_db()


    def __validate_output_table(self):
        _returned = None

        try:
            self.__open_db()
            self.__db_exec('select * from output_devices')
        except sqlite3.OperationalError as oe:
            self.__db_cursor.execute(
                    'create table output_devices '+\
                    '(device string not null, '+\
                    ' output_item string not null,'+\
                    ' file_name string, '+\
                    ' primary key (device, output_item))'
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
            self.add_output_device(devicename=devicename,
                                  output_item='Default audio device',
                                  file_name='datavolume/'+devicename+\
                                    '-default-audio.txt')
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
            self.__db_exec('delete from output_devices where device = ?',
                           (devicename,))
            self.__db_conn.commit()
        except:
            raise
        finally:
            self.__close_db()

        return True


    def add_output_device(self,
                          devicename=None,
                          output_item=None,
                          file_name=None
    ):
        try:
            if devicename == None or output_item == None or file_name == None:
                return None

            self.__open_db()
            self.__db_exec('insert or replace into '+\
                           'output_devices values (?, ?, ?)',
                           (devicename, output_item, file_name))
            self.__db_conn.commit()
        except:
            raise
        finally:
            self.__close_db()

        return True

    def remove_output_device(self, devicename=None, output_item=None):
        try:
            if devicename == None or output_item == None:
                return False

            self.__open_db()
            self.__db_exec('delete from output_devices '+\
                           'where device = ? '+\
                           'and output_item = ?',
                           (devicename, output_item))
            self.__db_conn.commit()
        except:
            raise
        finally:
            self.__close_db()

        return True


    def get_output_devices(self, devicename=None):
        if devicename == None:
            return []

        returned = []
        try:
            self.__open_db()
            self.__db_exec('select output_item, file_name '+\
                           'from output_devices '+\
                           'where device = ?',
                           (devicename,))
            returned = self.__db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()

        return returned


    def get_output_device(self, devicename=None, output_item=None):
        if devicename == None or output_item == None:
            return []

        returned = []
        try:
            self.__open_db()
            self.__db_exec('select output_item, file_name '+\
                           'from output_devices '+\
                           'where device = ? '+\
                           'and output_item = ?',
                           (devicename, output_item))
            returned = self.__db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()

        return returned


