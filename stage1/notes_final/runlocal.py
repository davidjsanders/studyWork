"""
   See runserver.py
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

# ONLY used in runlocal.py NOT in runserver.py
# Run the server. host = '0.0.0.0' enables access from any endpoint (necessary
# for using with Docker), debug=True enables verbose debugging - not to be used
# in production.
app.run(host='0.0.0.0', port=int(Config.port_number), debug=True)
