import sqlite3, os

class v3_00_Pairing_Database(object):

    db_name = 'datavolume/pairing.db'
    db_conn = None
    db_cursor = None
    server_name = None
    port_number = None

    def __init__(self, server_name=None, port_number=None):
        self.server_name = server_name
        self.port_number = port_number

        self.db_name = 'datavolume/'+server_name+'-'+\
            str(port_number)+'-pairing.db'
        self.db_conn = None
        self.db_cursor = None

        self.validate_pairing_table()
        self.validate_output_table()


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


    def validate_pairing_table(self):
        _returned = None

        try:
            self.open_db()
            self.db_exec('delete from paired_devices')
            self.db_conn.commit()
        except sqlite3.OperationalError as oe:
            self.db_cursor.execute(
                    'create table paired_devices '+\
                    '(device string not null primary key, key string)'
                )
        except Exception as e:
            print(repr(e))
            raise
        finally:
            self.close_db()


    def validate_output_table(self):
        _returned = None

        try:
            self.open_db()
            self.db_exec('delete from output_devices')
            self.db_conn.commit()
        except sqlite3.OperationalError as oe:
            self.db_cursor.execute(
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


    def check_pairing(self, devicename):
        returned = None
        try:
            self.open_db()
            self.db_exec('select key from paired_devices where device = ?',
                           (devicename,))
            returned = self.db_cursor.fetchall()
            if not returned == []:
                if type(returned) == list:
                    returned = returned[0][0]

        except Exception as e:
            print(repr(e))
        finally:
            self.close_db()

        return returned

    def pair_device(self, devicename):
        try:
            pairing_key = '1234-5678-9012-3456'

            self.open_db()
            self.db_exec('insert or replace into '+\
                           'paired_devices values (?, ?)',
                           (devicename, pairing_key))
            self.db_conn.commit()
            self.add_output_device(devicename=devicename,
                                  output_item='Default audio device',
                                  file_name='datavolume/'+devicename+\
                                    '-default-audio.txt')
        except:
            raise
        finally:
            self.close_db()

        return pairing_key

    def remove_pairing(self, devicename):
        try:
            self.open_db()
            self.db_exec('delete from paired_devices where device = ?',
                           (devicename,))
            self.db_exec('delete from output_devices where device = ?',
                           (devicename,))
            self.db_conn.commit()
        except:
            raise
        finally:
            self.close_db()

        return True


    def add_output_device(self,
                          devicename=None,
                          output_item=None,
                          file_name=None
    ):
        try:
            if devicename == None or output_item == None or file_name == None:
                return None

            self.open_db()
            self.db_exec('insert or replace into '+\
                           'output_devices values (?, ?, ?)',
                           (devicename, output_item, file_name))
            self.db_conn.commit()
        except:
            raise
        finally:
            self.close_db()

        return True

    def remove_output_device(self, devicename=None, output_item=None):
        try:
            if devicename == None or output_item == None:
                return False

            self.open_db()
            self.db_exec('delete from output_devices '+\
                           'where device = ? '+\
                           'and output_item = ?',
                           (devicename, output_item))
            self.db_conn.commit()
        except:
            raise
        finally:
            self.close_db()

        return True


    def get_output_devices(self, devicename=None):
        if devicename == None:
            return []

        returned = []
        try:
            self.open_db()
            self.db_exec('select output_item, file_name '+\
                           'from output_devices '+\
                           'where device = ?',
                           (devicename,))
            returned = self.db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.close_db()

        return returned


    def get_output_device(self, devicename=None, output_item=None):
        if devicename == None or output_item == None:
            return []

        returned = []
        try:
            self.open_db()
            self.db_exec('select output_item, file_name '+\
                           'from output_devices '+\
                           'where device = ? '+\
                           'and output_item = ?',
                           (devicename, output_item))
            returned = self.db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.close_db()

        return returned


