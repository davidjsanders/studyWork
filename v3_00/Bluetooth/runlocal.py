"""
    Application: notes_final
    ------------------------------------------------------------------------
    Author:      David J. Sanders
    Student No:  H00035340
    Date:        
    ------------------------------------------------------------------------
    Overivew:    To do

    Purpose:     To do

    Patterns:    Larger Applications pattern from Flask website (Ronacher,
                 2013)

    App Structure
    -------------

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

# Import the app, and api modules from the notes app (__init__.py) so that
# they can be accessed globally by any module within this package.
from Bluetooth import app, api
from Bluetooth_Boundary import apiR

app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

