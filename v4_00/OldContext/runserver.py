"""
    Application: Context
    ------------------------------------------------------------------------
    Author:      David J. Sanders
    Student No:  H00035340
    Date:        DD Mon YYYY
    ------------------------------------------------------------------------
    Overivew:    The Context description goes here.
                 ** Replace Context with the context name in ALL files.
                 ** bin/build.sh and bin/push.sh - context is ALL lowercase!

    Patterns:    Larger Applications pattern from Flask website (Ronacher,
                 2013)


    Revision History
    --------------------------------------------------------------------------
    Date         | By             | Reason
    --------------------------------------------------------------------------
    28 Mar 2016  | D Sanders      | First version.


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
# Import the context Api from the flask_restful package
from flask_restful import Api

# Import the app, and api contexts from the Context app (__init__.py) so that
# they can be accessed globally by any context within this package.
from Context import app, api


