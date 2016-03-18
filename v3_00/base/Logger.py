import datetime, requests, json
from textwrap import wrap

class Logger(object):
    __filename=None
    __sender=None
    __central_logger=None
    __controller=None

    def __init__(self,
                 controller=None,
                 filename='logfile.txt',
                 sender='unknown'
    ):
        if controller == None:
            raise Exception('Controller cannot be None!')

        self.__controller = controller
        self.__filename = filename
        self.__sender = sender

        self.writelog('INITIALIZE LOG: {0}'.format(self.__filename))
        self.writelog('SENDER: {0}'.format(self.__sender))


    def __now(self):
        return datetime.datetime.now()


    def file_clear(self):
        try:
            f = open(self.__filename, 'a')
            f.write("{0:>28s}\n".format(str(now)+': log cleared.'))
        except Exception:
            raise
        finally:
            if not f == None:
                f.close()


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
        central_logger = self.__controller.kvstore.get_key('logger')
        if log_to_central and not (central_logger in ('', [], None)):
            try:
                self.db_logger(log_message=log_message, logger=central_logger)
            except requests.exceptions.ConnectionError as rce:
                pass # Ignore communication errors
            except Exception:
                raise


    def db_logger(self,
                  log_message=None,
                  logger=None
    ):
        if logger == None:
            return
        try:
            payload_data = {
                "sender":self.__sender,
                "log-type":"normal",
                "message":log_message
            }
            requests.post(
                logger,
                data=json.dumps(payload_data),
                timeout=10 # If nothing after 10s. ignore central
            ) # Ignore return from central logger
        except Exception as e:
            self.writelog(log_message='Exception: {0}'.format(repr(e)),
                          log_to_central=False)
            pass



