import sqlite3

class v3_00_Location_Service_Database(object):
    db_name = None
    db_conn = None
    db_cursor = None

    def __init__(self, server_name=None, port_number=None):
        if server_name == None:
            server = 'localhost'
        else:
            server = server_name
        if port_number == None:
            port_number = '5000'
        else:
            port_number = str(port_number)

        self.db_name = 'datavolume/'+server+'-'+\
            port_number+'-locserv.db'
        self.db_conn = None
        self.db_cursor = None

        self.validate_hotspots_table()


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


    def validate_hotspots_table(self):
        _returned = None

        try:
            self.open_db()
            self.db_exec('delete from hotspots')
        except sqlite3.OperationalError as oe:
            print(str(oe))
            self.db_cursor.execute(
                    'CREATE TABLE hotspots( '+\
                    '  location string not null primary key,'
                    '  upperX real not null, '+\
                    '  upperY real not null, '+\
                    '  lowerX real not null, '+\
                    '  lowerY real not null, '+\
                    '  description string not null'
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


    def set_hotspot(
        self,
        location=None,
        upperX=None,
        upperY=None,
        lowerX=None,
        lowerY=None,
        description=None
    ):
        if location == None \
        or upperX == None \
        or upperY == None \
        or lowerX == None \
        or lowerY == None \
        or description == None:
            return False

        returned = False
        try:
            self.open_db()
            self.db_exec('insert or replace into hotspots '+\
                           'values (?, ?, ?, ?, ?, ?)',
                           (location,
                            upperX, 
                            upperY, 
                            lowerX, 
                            lowerY, 
                            description)
                          )
            self.db_conn.commit()
            returned = True
        except Exception as e:
            print(repr(e))
        finally:
            self.close_db()
            return returned


    def get_hotspots(self):
        try:
            self.open_db()
            self.db_exec('select * from hotspots')
            returned = self.db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.close_db()
            if returned == []:
                returned = None

        return returned


    def get_hotspot_by_name(self, location=None):
        if location == None:
            return None

        try:
            self.open_db()
            self.db_exec('select * from hotspots '+\
                           'where location = ?',
                           (location,)
                          )
            returned = self.db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.close_db()
            if returned == []:
                returned = None

        return returned


    def get_hotspot_by_location(self, x=None, y=None):
        if x == None or y == None:
            return None

        try:
            self.open_db()
            self.db_exec('select * from hotspots '+\
                           'where (? >= lowerX and ? <= upperX) '+\
                           'and (? >= lowerY and ? <= upperY)',
                           (x, x, y, y)
                          )
            returned = self.db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.close_db()
            if returned == []:
                returned = None

        return returned


    def clear_hotspot(
        self,
        location=None
    ):
        if location == None:
            return False

        returned = False
        try:
            self.open_db()
            self.db_exec('delete from hotspots '+\
                           'where location = ? ',
                           (location,)
            )
            self.db_conn.commit()
            returned = True
        except Exception as e:
            print(repr(e))
        finally:
            self.close_db()

        return returned

