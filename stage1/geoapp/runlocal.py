"""
    Application: notes_final
    ------------------------------------------------------------------------
    Author:      David J. Sanders
    Student No:  H00035340
    Date:        22 November 2015
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
# Import the module Api from the flask_restful package
from flask_restful import Api

# Import the app, and api modules from the notes app (__init__.py) so that
# they can be accessed globally by any module within this package.
from geoapp import app, api

# Import the configuration module
#import geoapp.resources.Config as Config

# Import the OS package to access environment variables
import os

# Set the port_number to whatever portToUse is
#Config.port_number = os.environ['portToUse']
#Config.initialize()
app.run(host='0.0.0.0', debug=True)
