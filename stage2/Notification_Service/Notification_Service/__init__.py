"""
    Module:      __init__.py
    Overivew:    The initialization module of the package notes.
    Purpose:     Define the app and api variables.
                 Import the main.py main module.
    Patterns:    Larger Applications pattern from Flask website (Ronacher,
                 2013)

    References
    ----------
    Ronacher, A., 2013, 'Larger Applications' [ONLINE]. Available at: 
    http://flask.pocoo.org/docs/0.10/patterns/packages/ (Accessed: 04 November 
    2015)

"""
# Import the module Flask from the flask package
from flask import Flask

# Import the module Api from the flask_restful package
from flask_restful import Api

# Import werkzueg
from werkzeug import serving

# Import the threading module
import threading

# Import PairControl
from Notification_Service import Control
#from Notification_Service import Notification_Control
from Notification_Service import Notification_Receiver
from Notification_Service import Notification_Processor
from Notification_Service import Notification_Push_Control

# The app is this application and set when the Python file is run from the
# command line, e.g. python3 /some/folder/notes/runserver.py
app = Flask(__name__)
# Create an Api object inheriting app
api = Api(app)

#Setup objects for pairing and broadcasting.
#notification_control_object = Notification_Control.Notification_Control_v1_00()
notification_receiver_object = \
    Notification_Receiver.Notification_Receiver_v1_00()
notification_push_control = \
    Notification_Push_Control.Notification_Push_Control_v1_00()
control = Control.Control_v1_00()

# Setup threaded background job
# Check app is NOT reloaded or spawned
# Reference: http://werkzeug.pocoo.org/docs/0.10/serving/#werkzeug.serving.is_running_from_reloader
#
if not serving.is_running_from_reloader():
    thread_job = threading.Thread(
        target=Notification_Processor.redis_processor,
        args=(control,)
    )
    thread_job.setDaemon(True)
    thread_job.start()

# Import the main.py module
import Notification_Service.main

