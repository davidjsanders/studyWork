import requests
import json
import time
from datetime import datetime

def location_processor(control_object=None):
    while True:
        state = control_object.get_state()
        if state.upper() == 'ON':
            do_location_check(control_object)
        time.sleep(30)

def do_location_check(control_object=None):
    recipient = control_object.get_value('recipient')
    if recipient == None:
        return

    try:
        payload_data = {
            "key":"1234-5678-9012-3456"
        }
        request_response = requests.get(
            recipient+'/location',
            data=json.dumps(payload_data)
        )
        if request_response.status_code in (200,201):
            returned_data = request_response.json()
            if returned_data['response'] == 'success':
                x = returned_data['data']['x']
                y = returned_data['data']['y']
                xy = (x, y)
                if xy == (22.123, 211.072):
                    timeNow = time.time()
                    timeThen = None
                    issue_notification = True

                    lastXY = control_object.get_value(str(xy))

                    if lastXY == None:
                        lastXY = control_object.set_value(str(xy), str(timeNow))
                    else:
                        timeString = time.ctime(lastXY)
                        tempTime = datetime.strptime(timeString,
                                                     '%a %b %d %H:%M:%S %Y')
                        timeThen = time.mktime(tempTime.timetuple())
                        timePassed = timeNow - timeThen
                        if timePassed < (60 * 5):    # 60 * 5 = 5 minutes
                            issue_notification = False
                        else:
                            control_object.set_value(str(xy), str(timeNow))

                    if issue_notification:
                        raise_location_notification(
                            control_object=control_object,
                            recipient=recipient,
                            xy=xy,
                            timeStamp=str(time.ctime(timeNow))
                        )
    except requests.exceptions.ConnectionError as rce:
        print(rce)
    except Exception as e:
        print(e)
        raise


def raise_location_notification(
    control_object=None,
    recipient=None,
    timeStamp=None,
    xy=()
):
    try:
        service = control_object.get_value('service')
        if service == None:
            return

        payload_data = {
            "key":"1234-5678-9012-3456",
            "message":"You have entered an area known for high rates of STI "+\
                "infections and drug use. Remember: Safe sex is good sex!",
            "sender":"Monitor_App",
            "recipient":recipient+'/notification',
            "action":"openMap{0}".format(xy)
        }
        request_response = requests.post(
            service+'/notification',
            data=json.dumps(payload_data)
        )
        log_string = str(request_response.status_code) + ': ' + \
                     str(request_response.json())
        control_object.print_error(log_string)
    except Exception as e:
        print(repr(e))



