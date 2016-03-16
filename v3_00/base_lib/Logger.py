import datetime, requests, json
from textwrap import wrap

class Logger(object):
    __filename=None
    __sender=None
    __central_logger=None

    def __init__(self, filename=None, sender=None):
        if filename==None:
            self.__filename='logfile.txt'
        else:
            self.__filename=filename
        if sender == None:
            self.__sender = 'UNKNOWN'
        else:
            self.__sender = sender

        self.writelog('INITIALIZE LOG: {0}'.format(self.__filename))
        self.writelog('SENDER: {0}'.format(self.__sender))


    def __now(self):
        return datetime.datetime.now()


    def get_central_logger(self):
        return self.__central_logger


    def set_central_logger(self, logger=None):
        self.__central_logger = logger


    def writelog(self, 
                 log_message=None,
                 log_to_central=True
    ):
        now = self.__now()
        f = None
        try:
            f = open(self.__filename, 'a')
            if log_message == None or log_message == '':
                f.write("{0:>28s}\n".format(str(now)+': '))
            else:
                wrapped80 = wrap(log_message, 79)
                time_line = [str(now)]
                for line in wrapped80:
                    time_line.append('')
                for i, line in enumerate(wrapped80):
                    f.write('{0:>28s}{1}'.format(time_line[i]+': ', line)+"\n")
        except Exception:
            raise
        finally:
            if not f == None:
                f.close()
        if log_to_central and not (self.__central_logger == None):
            try:
                self.db_logger(log_message=log_message)
            except requests.exceptions.ConnectionError as rce:
                pass # Ignore communication errors
            except Exception:
                raise


    def db_logger(self,
                  log_message=None
    ):
        if self.__central_logger == None:
            return
        try:
            payload_data = {
                "sender":self.__sender,
                "log-type":"normal",
                "message":log_message
            }
            requests.post(
                self.__central_logger,
                data=json.dumps(payload_data),
                timeout=10 # If nothing after 10s. ignore central
            ) # Ignore return from central logger
        except Exception as e:
            self.writelog(log_message='Exception: {0}'.format(repr(e)),
                          log_to_central=False)
            raise



