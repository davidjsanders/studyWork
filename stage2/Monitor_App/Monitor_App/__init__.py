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

# Import atexit
import atexit

# Import the threading module
import threading

# Import PairControl
from Monitor_App import Control
from Monitor_App import State_Control
from Monitor_App import App_Launched_Control
from Monitor_App import Location_Processor

# The app is this application and set when the Python file is run from the
# command line, e.g. python3 /some/folder/notes/runserver.py
app = Flask(__name__)
# Create an Api object inheriting app
api = Api(app)

#Setup objects for pairing and broadcasting.
#notification_control_object = Notification_Control.Notification_Control_v1_00()
state_control = State_Control.State_Control_v1_00()
app_launched_control = App_Launched_Control.App_Launched_Control_v1_00()
control = Control.Control_v1_00()

# Setup threaded background job
# Check app is NOT reloaded or spawned
# Reference: http://werkzeug.pocoo.org/docs/0.10/serving/#werkzeug.serving.is_running_from_reloader
#
if not serving.is_running_from_reloader():
    thread_job = threading.Thread(
        target=Location_Processor.location_processor,
        args=(control,)
    )
    thread_job.setDaemon(True)
    thread_job.start()

    # Reference https://docs.python.org/2/library/atexit.html
    # Register an exit handler - in case we need to do any close out stuff on
    # our thread.
#    atexit.register(Notification_Processor.redis_close,
#                    thread=thread_job,
#                    controller=control)

# Import the main.py module
import Monitor_App.main

