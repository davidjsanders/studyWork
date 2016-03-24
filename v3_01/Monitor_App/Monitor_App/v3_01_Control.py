from Monitor_App.v3_00_Control import v3_00_Control

class v3_01_Control(v3_00_Control):
    log_file = None
    Monitor_App_db = None
    config_logger = None

    def __init__(self):
        super(v3_01_Control, self).__init__()

        # v3_01 Changes
        self.log('Setting default messages')
        self.set_value('app_msg',
                       '!*! {0} launched !*!'+\
                           '. Remember: Safe sex is good sex!')
        self.set_value('location_msg',
                       '!*! Hotspot detected at {0} !*!'+\
                           '. Remember: Safe sex is good sex!')
        self.set_value('default_app_msg', self.get_value('app_msg'))
        self.set_value('default_location_msg', self.get_value('location_msg'))
        self.log('Setting default messages - done.')


    def get_app_message(self):
        return_value = self.get_value('app_msg')
        if return_value in (None, '', []):
            return_value = self.get_value('default_app_msg')
        return return_value


    def set_app_message(self, text=None):
        return_value = self.set_value('app_msg', text)
        if return_value in (None, '', []):
            return_value = self.get_value('default_app_msg')
        return return_value


    def get_location_message(self):
        return_value = self.get_value('location_msg')
        if return_value in (None, '', []):
            return_value = self.get_value('default_location_msg')
        return return_value


    def set_location_message(self, text=None):
        return_value = self.set_value('location_msg', text)
        if return_value in (None, '', []):
            return_value = self.get_value('default_location_msg')
        return return_value

