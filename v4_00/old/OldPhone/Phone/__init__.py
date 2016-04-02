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

# The app is this application and set when the Python file is run from the
# command line, e.g. python3 /some/folder/notes/runserver.py
app = Flask(__name__)

# Create an Api object inheriting app
api = Api(app)

# Import the main.py module
import Phone.main

