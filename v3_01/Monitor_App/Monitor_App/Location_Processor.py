import requests
import json
import time
from datetime import datetime

def location_processor(control_object=None):
    while True:
        state = control_object.get_state()
        if state.upper() == 'ON': # Only check if we've been switched on.
            do_location_check(control_object)
        time.sleep(30) # Only check every 30 seconds.

def do_location_check(control_object=None):
    recipient = control_object.get_value('recipient')
    if recipient == None:
        return

    try:
        payload_data = {
            "key":"1234-5678-9012-3456"
        }

        location_service = control_object.get_value('location-service')
        location_provider = control_object.get_value('location-provider')
        if location_service in (None, [], ''):
            control_object.log('Location check requested but there is '+\
                                  'no location service defined.')
            return

        control_object.log('Location requested from {0}.'\
            .format(location_provider)
        )
        request_response = requests.get(
            location_provider,
            data=json.dumps(payload_data)
        )
        control_object.log('Location request returned {0}:{1}'\
            .format(request_response.status_code,
                    request_response.text)
        )
        if request_response.status_code in (200,201):
            returned_data = request_response.json()
            if returned_data['response'] == 'success':
                x = returned_data['data']['x']
                y = returned_data['data']['y']
                control_object.log('Location request returned ({0},{1}).'\
                    .format(x, y))

                payload_data = {
                    "key":"1234-5678-9012-3456", "x":x, "y":y
                }
                control_object.log(
                    'Location Request checking if location ({0},{1})'\
                    .format(x, y)+' is in hotspot. '+\
                    'Checking with {0}'.format(location_service)
                    )

                check_response = requests.get(
                    location_service,
                    params=payload_data
                )

                control_object.log('URL is {0}'.format(check_response.url))

                control_object.log('Hotspot check returned {0}:{1}'\
                    .format(check_response.status_code, check_response.text)
                )
                if check_response.status_code in (200,201)\
                and check_response.json()['response'] == 'success':
                    xy = (x, y)
                    hotspot_yn = check_response.json()['data']['hotspot']
                    issue_notification = False
                    if hotspot_yn:
                        control_object.log(
                            'Location ({0},{1}) '.format(x, y)+\
                            'is in a hotspot. Now checking last reported time.')
                        timeNow = time.time()
                        timeThen = None
                        issue_notification = True

                        lastXY = control_object.get_value(str(xy))

                        if lastXY == None:
                            lastXY = control_object.set_value(str(xy),
                                                              str(timeNow))
                            control_object.log(
                                'Location ({0},{1}) '.format(x, y)+\
                                'has not been previously encountered.')
                        else:
                            timeString = time.ctime(lastXY)
                            tempTime = datetime.strptime(timeString,
                                                         '%a %b %d %H:%M:%S %Y')
                            timeThen = time.mktime(tempTime.timetuple())
                            timePassed = timeNow - timeThen
                            if timePassed < (60 * 5):    # 60 * 5 = 5 minutes
                                control_object.log(
                                    'Location ({0},{1}) '.format(x, y)+\
                                    'reported less than 5 minutes ago.')
                                issue_notification = False
                            else:
                                control_object.log(
                                    'Location ({0},{1}) '.format(x, y)+\
                                    'reported more than 5 minutes ago.')
                                control_object.set_value(str(xy), str(timeNow))
                    else:
                        control_object.log(
                            'Location ({0},{1}) '.format(x, y)+\
                            'is not in a hotspot')

                    if issue_notification:
                        raise_location_notification(
                            control_object=control_object,
                            recipient=recipient,
                            xy=xy,
                            timeStamp=str(time.ctime(timeNow))
                        )
                else:
                    control_object.log(
                        'Location check returned {0}: {1}'\
                           .format(check_response.status_code,
                                   check_response.json()))
    except requests.exceptions.ConnectionError as rce:
        control_object.log('Exception {0}) '.format(str(rce)))
    except Exception as e:
        control_object.log('Exception {0}) '.format(repr(e)))


def raise_location_notification(
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
                'cannot be raised as there is no notification service provider')
            return

        message_to_send = control_object.get_location_message()\
            .format(application)

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



