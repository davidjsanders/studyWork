# Import base library modules - From Bluetooth symbolic link to /base_lib
import base_lib
from base_lib.Responder import Responder
from base_lib.Config_Logger import Config_Logger
from base_lib.Logger import Logger
from base_lib.Environment import Environment
from base_lib.KVStore import KVStore

# Import general modules and packages
from Bluetooth import Pairing_Database

#
# SuperClass.
# ----------------------------------------------------------------------------
class v3_00_Control(object):
    log_file = None
    pairing_db = None
    responder = None
    config_logger = None

    def __init__(self):
        # Setup environment
        self.environment = Environment()
        port_number = self.environment['port_number']
        server_name = self.environment['server_name']
        host_ip = self.environment['ip_addr']
        version = self.environment['version']
        pre_filename = 'datavolume/{0}-{1}'\
                       .format(server_name, port_number)

        # Setup Config for Logger
        # self.config_logger = Config_Logger(self)

        # Setup responder
        self.responder = Responder()
        self.do_response = self.responder.do

        # Setup KV Store
        self.kvstore = KVStore(pre_filename+'-config.db')
        self.get_value = self.kvstore.get_key
        self.set_value = self.kvstore.set_key
        self.clear_value = self.kvstore.clear_key

        # Setup Logger
        self.logger = Logger(controller=self,
                             filename=pre_filename+'-log.txt',
                             sender='Bluetooth-{1}'\
                                 .format(server_name, port_number))
        self.logger.writelog('Log written')
        self.log = self.logger.writelog
        self.db_logger = self.logger.db_logger


        # General startup
        self.server_name = server_name
        self.port_number = port_number

        # Setup the pairing database
        self.pairing_db = Pairing_Database.Pairing_Database(
            server_name = self.server_name,
            port_number = self.port_number
        )

        self.log('Bluetooth Device {0}:{1} Started'\
                 .format(server_name, port_number))

        self.log('Setting environment variables to {0}'\
            .format(self.environment))
        self.set_value('server_name', server_name)
        self.set_value('port_number', port_number)
        self.set_value('ip_addr', host_ip)
        self.set_value('version', version)
        self.log('Stored environment variables')


    def get_pairing_db(self):
        return self.pairing_db

