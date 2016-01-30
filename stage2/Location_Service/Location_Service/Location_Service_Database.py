import sqlite3

class Location_Service_Database(object):
    __db_name = None
    __db_conn = None
    __db_cursor = None

    def __init__(self):
        self.__db_name = 'datavolume/Location_Service.db'
        self.__db_conn = None
        self.__db_cursor = None

        self.__validate_hotspots_table()


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


    def __validate_hotspots_table(self):
        _returned = None

        try:
            self.__open_db()
            self.__db_exec('select * from hotspots')
        except sqlite3.OperationalError as oe:
            print(str(oe))
            self.__db_cursor.execute(
                    'CREATE TABLE hotspots( '+\
                    '  upperX real not null, '+\
                    '  upperY real not null, '+\
                    '  lowerX real not null, '+\
                    '  lowerY real not null, '+\
                    '  description string not null, '+\
                    '  primary key (upperX, upperY, lowerX, lowerY)'
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


    def set_hotspot(
        self,
        upperX=None,
        upperY=None,
        lowerX=None,
        lowerY=None,
        description=None
    ):
        if upperX == None \
        or upperY == None \
        or lowerX == None \
        or lowerY == None \
        or description == None:
            return False

        returned = False
        try:
            self.__open_db()
            self.__db_exec('insert or replace into hotspots '+\
                           'values (?, ?, ?, ?, ?)',
                           (upperX, upperY, lowerX, lowerY, description)
                          )
            self.__db_conn.commit()
            returned = True
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()
            return returned


    def get_hotspots(self):
        try:
            self.__open_db()
            self.__db_exec('select * from hotspots')
            returned = self.__db_cursor.fetchall()
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()
            if returned == []:
                returned = None

        return returned

    def clear_hotspot(
        self,
        upperX=None,
        upperY=None,
        lowerX=None,
        lowerY=None
    ):
        if upperX == None \
        or upperY == None \
        or lowerX == None \
        or lowerY == None \
        or description == None:
            return False

        returned = False
        try:
            self.__open_db()
            self.__db_exec('delete from hotspots '+\
                           'where upperX = ? '+\
                           'and upperY = ? '+\
                           'and lowerX = ? '+\
                           'and lowerY = ? ',
                           (upperX, upperY, lowerX, lowerY)
            )
            self.__db_conn.commit()
            returned = True
        except Exception as e:
            print(repr(e))
        finally:
            self.__close_db()

        return returned

