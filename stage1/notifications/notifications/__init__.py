"""
    module: __init__.py
    ------------------------------------------------------------------------
    Author:      David J. Sanders
    Student No:  H00035340
    Last Update: 15 December 2015
    Update:      Revise documentation
    ------------------------------------------------------------------------
    Overivew:    The module called when runserver.py is executed using the
                 uWSGI service.

    Purpose:     Launches the application

    Called By:   n/a

    Patterns:    Larger Applications pattern from Flask website (Ronacher,
                 2013)

    References
    ----------
    Ronacher, A., 2013, 'Larger Applications' [ONLINE]. Available at: 
        http://flask.pocoo.org/docs/0.10/patterns/packages/ (Accessed: 04 
        November 2015)
"""
# Import the module Flask from the flask package
from flask import Flask

# Import the module Api from the flask_restful package
from flask_restful import Api

# The application context
app = Flask(__name__)

# Create an Api object using app
api = Api(app)

# Import the main.py module and run the program
import notifications.main
