"""
    Application: Logger
    ------------------------------------------------------------------------
    Author:      David J. Sanders
    Student No:  H00035340
    Date:        26 Jan 2016
    ------------------------------------------------------------------------
    Overivew:    The Logger application models a Logger handsfree 
                 device which can be paired to any number of other devices
                 and then used to broadcast a message. The applicaiton writes
                 the broadcasted message to a file which anyone can see 
                 (analogous to anyone being able to hear an announced message)

    Patterns:    Larger Applications pattern from Flask website (Ronacher,
                 2013)

    App Structure
    -------------
    /Logger                     - Root directory.
       runserver.py                - this file.
       startup.sh                  - the startup command when containerized.
     * Logger_uwsgi.ini         - UWSGI ini file - only in container.
     * Logger_uwsgi.conf        - UWSGI config file - only in container.
     - /bin                        - start, stop, & build - NOT in container.
       /Logger                  - Package root.
            Broadcast_Control.py   - The Broadcast controller.
            Control.py             - General (or helper) controller.
            __init__.py            - Python initialization file for package.
            main.py                - Define routes for version control info.
            Pairing_Control.py     - The controller for pairing/un-pairing.
            Pairing_Database.py    - Persistance logic.
       /Logger_Boundary         - The boundary interfaces.
            Broadcast_Boundary.py  - The Broadcast boundary (POST).
            __init__.py            - Python initialization file for package.
            main.py                - Define routes for boundaries.
            Pair_Boundary.py       - The Pair boundary (GET,POST,DELETE).
            Versions_Boundary.py   - The Version Info boundary (GET).
       /datavolume                 - The persistent folder for containerization


    Revision History
    --------------------------------------------------------------------------
    Date         | By             | Reason
    --------------------------------------------------------------------------
    24 Jan 2015  | D Sanders      | First version.


    References
    ----------
    Ronacher, A., 2013, 'Larger Applications' [ONLINE]. Available at: 
    http://flask.pocoo.org/docs/0.10/patterns/packages/ (Accessed: 04 November 
    2015)
    Souren, K., 2015, 'What is __init__.py for?' [ONLINE]. Available at:
    http://stackoverflow.com/questions/448271/what-is-init-py-for (Accessed:
    04 November 2015)

"""
import threading
# Import the module Api from the flask_restful package
from flask_restful import Api

# Import the app, and api modules from the Logger app (__init__.py) so that
# they can be accessed globally by any module within this package.
from Logger import app, api

# Import the boundary apiR module
from Logger_Boundary import apiR

# UNCOMMENT to run locally
#app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

