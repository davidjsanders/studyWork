from Bluetooth import Control, Pairing_Control
import datetime, time, json

#
# SuperClass.
# ----------------------------------------------------------------------------
class Broadcast_Control(object):
    __output_devices = []
    __controller = Control.global_control

    def broadcast_message(self, devicename='Unknown', text=None, key=None):
        success = 'success'
        status = '200'
        message = 'Message has been broadcast.'
        data = {"device":devicename,
                "action":"broadcast",
                "message":text}

        self.__controller.log(log_message='Broadcast request from "{0}"'\
            .format(devicename))

        pair_control_object = Pairing_Control.global_pair_control

        pairing_key = pair_control_object.check_pairing(devicename)

        if pairing_key == []:
            success = 'error'
            status = '404'
            message = 'Device is not paired'
            pairing_key = None
            self.__controller.log(
                log_message='Broadcasting error: {0}'\
                    .format(message))
        elif pairing_key != key:
            success = 'error'
            status = '403'
            message = 'Device pairing key is incorrect!'
            pairing_key = None
            self.__controller.log(
                log_message='Broadcasting error: {0}'\
                    .format(message))
        elif text == '' or text == None:
            success = 'error'
            status = '400'
            message = 'Cannot broadcast an empty message'
            pairing_key = None
            self.__controller.log(
                log_message='Broadcasting error: {0}'\
                    .format(message))
        else:
            try:

                self.__controller.log(
                     log_message='Broadcasting "{0}" on behalf of "{1}"' \
                        .format(text, devicename))

                now = datetime.datetime.now()
                tz = time.tzname[0]
                tzdst = time.tzname[1]

                self.__output_devices = pair_control_object.get_output_devices(
                    devicename
                )

                for outputfile in self.__output_devices:
                    f = open(outputfile[1],'a')
                    f.write(('-'*80)+"\n")
                    f.write('Bluetooth output device: {0}'\
                            .format(outputfile[0])+"\n")
                    f.write(('-'*80)+"\n")
                    f.write('Broadcast from: {0}'.format(devicename)+"\n")
                    f.write('Broadcast at: {0} ({1}/{2})'\
                        .format(now, tz, tzdst)+"\n")
                    f.write('Message: {0}'.format(text)+"\n\n")
                    f.close()

            except:
                raise

        self.__controller.log(
            log_message='Broadcasting on behalf of "{0}" finished. ({1} {2})'\
                .format(devicename, success, status))

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value

global_broadcast_control = Broadcast_Control()
