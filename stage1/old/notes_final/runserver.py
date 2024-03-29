"""
    Application: notes_final
    ------------------------------------------------------------------------
    Author:      David J. Sanders
    Student No:  H00035340
    Date:        09 November 2015
    ------------------------------------------------------------------------
    Overivew:    A demonstration of a device, such as a smart phone, which
                 provides notifications and changes the behaviour of the
                 notifications based on certain configurations:

                  Mode  Description
                     1  No notifications when locked
                     2  Locked or unlocked status
                     3  Sensitivity checking

                 For the first config, notifications do not show if the device
                 is locked. This is as per Android, prior to Lollipop.

                 For the second config, notifications show whether the device
                 is locked or unlcoked as per current Apple iOS (v9 at date of
                 writing), Android (Lollipop at date of publication), and 
                 Windows Phone (8.1 at date of writing).

                 For the third config, notifications are checked for a
                 sensitivity sentinel which, if set to high, prevents a
                 notification being shown on the lock screen. This is as per
                 Android (Lollipop and later) but not applicable to iOS devices
                 or Windows Phone.

                 To query (GET) the mode of the application call:

                   http://<theappurl>:<port>/mode

                 (append /9 where 9 is 1, 2, or 3, to set with method PUT)

    Purpose:     To demonstrate how a solution could be modelled by developing
                 a skeleton version of the application using any language, in
                 this case Python. The model is relatively easy to build and
                 simulation occurs through the building and executing of the
                 application modules in Docker to minimize dependency issues.
                 Python was selected for its ability to easily deliver both
                 object-oriented designs and for the RESTful extensions
                 provided by flask_restful. The application demonstrates the
                 use of hypertext as the engine of application state (HATEOAS)
                 and will be used in the second stage model.

    Patterns:    Larger Applications pattern from Flask website (Ronacher,
                 2013)

    App Structure
    -------------
    notes_final.ini       - Python app server
    README.1ST            - Instructions to install and use this app
    runlocal.sh           - Run the app locally (see README.1ST) using uWSGI
    runlocal.py           - Run the app locally (see README.1ST) using Python3
    runserver.py          - application core
    startup.sh            - Startup shell used by Docker container to execute
                            application
    bin/                  - Utilities directory
        build.sh          - Docker: build the container
        create.sh         - Docker: create x containers-> bin/create.sh 5
                          -         initializes 5 containers starting at port
                          -         5000, therefor 5000,5001,5002,5003,5004
        destroy.sh        - Docker: destroy x containers (as above)
        run.sh            - Docker: run app. bin/run.sh <port> (default 5000)
        stop.sh           - Docker: stop app. bin/stop.sh <port> (default 5000)
    datavol/              - Docker: mounted in container as /notes/datavol
        notesuwsgi.db     - Sqlite3 database for notifications - thread safe
    notes/                - main directory
    notes/notes/          - package structure
        __init__.py       - ensures Python treats directories as packages, also
                            defines key global variables app and api (Souren,
                            2015)
        main.py           - the main module of the program
        resources/        - the resources (modules) folder
            Config.py        - the Config class
            Helper.py        - the Helper class
            Location.py      - the Location class - not used
            Lock.py          - the Lock and Unlock classes
            Notifications.py - the Notification, NotificationGetter, and 
                               NotificationAdder classes
            Persist.py       - the Persistance class, used to store and
                               retrieve notifications
        static/           - folder to contain static HTML pages (none used)
        templates/        - folder to contain templates (none used)

    References
    ----------
    Ronacher, A., 2013, 'Larger Applications' [ONLINE]. Available at: 
    http://flask.pocoo.org/docs/0.10/patterns/packages/ (Accessed: 04 November 
    2015)
    Souren, K., 2015, 'What is __init__.py for?' [ONLINE]. Available at:
    http://stackoverflow.com/questions/448271/what-is-init-py-for (Accessed:
    04 November 2015)

"""
# Import the module Api from the flask_restful package
from flask_restful import Api

# Import the app, and api modules from the notes app (__init__.py) so that
# they can be accessed globally by any module within this package.
from notes import app, api

# Import the configuration module
import notes.resources.Config as Config

# Import the OS package to access environment variables
import os

# Set the port_number to whatever portToUse is
Config.port_number = os.environ['portToUse']
Config.initialize()

