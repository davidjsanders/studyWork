from Monitor_App.v3_00_Location_Processor import v3_00_Location_Processor

import requests
import json
import time
from datetime import datetime

class v3_01_Location_Processor(v3_00_Location_Processor):

    def __init__(self):
        super(v3_01_Location_Processor, self).__init__()

    def raise_location_notification(
        self,
        control_object=None,
        recipient=None,
        timeStamp=None,
        xy=()
    ):
        try:
            control_object.log(
                'Location {0} '.format(xy)+' '\
                'hotspot notification being raised')

            service = control_object.get_value('service')

            if service == None:
                control_object.log(
                    'Location {0} '.format(xy)+' '\
                    'cannot be raised as there is no notification '+\
                    'service provider')
                return

            message_to_send = control_object.get_location_message()\
                                  .format(xy)

            payload_data = {
                "key":"1234-5678-9012-3456",
                "message":message_to_send,
                "sender":"Monitor_App",
                "recipient":recipient,
                "action":"openMap{0}".format(xy)
            }
            request_response = requests.post(
                service,
                data=json.dumps(payload_data)
            )
            log_string = str(request_response.status_code) + ': ' + \
                         str(request_response.json())
            control_object.log('Location notification request returned: {0}'\
                .format(log_string))
        except Exception as e:
            print(repr(e))

