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

    App Overview
    ------------
    The notifications app presents a model of a notifications engine in a
    smart device (e.g. a watch, or a phone). It allows notifications to be
    created, posted, and read. Running as a web service, the objective was to
    develop a model of the Besoain, et al., (2015) app which sends positive 
    behaviour reinforcing messages when a user runs a specific app or enters a 
    geolocation based hotspot.

    The app runs as a web service which responds to various get, put, post, and
    delete methods to enable notifications. It also connects to a bluetooth
    emulation which allows notifications to be 'broadcast'.

    For full overview see:

    1. README.1ST - The operating instructions for the service
    2. README.2ND - The guide to the model

    For simulation purposes, the service can be accessed by the interpreter.py
    application located in the test app.

    References
    ----------
    Besoain, F. et al., 2015. Prevention of sexually transmitted infections 
        using mobile devices and ubiquitous computing. International Journal of 
        Health Geographics, 14(1), pp. 1-12.
    Ronacher, A., 2013, 'Larger Applications' [ONLINE]. Available at: 
        http://flask.pocoo.org/docs/0.10/patterns/packages/ (Accessed: 04 
        November 2015)
    Souren, K., 2015, 'What is __init__.py for?' [ONLINE]. Available at:
        http://stackoverflow.com/questions/448271/what-is-init-py-for (Accessed:
        04 November 2015)

"""
# Import the module Api from the flask_restful package
from flask_restful import Api

# Import the app, and api modules from the notes app (__init__.py) so that
# they can be accessed globally by any module within this package.
from notifications import app, api

# Import the configuration module (effectively the library)
import notifications.resources.Config as Config

# Import the OS package to access environment variables
import os

# Set the port_number and server_name. If not defined, these will be updated in
# the config app to their defaults.
#
try:
    run_local_reached = False
    run_local_sentinel = False

    parameter_name = 'portToUse'
    Config.port_number = int(os.environ[parameter_name])

    parameter_name = 'serverName'
    Config.server_name = os.environ[parameter_name]

    run_local_reached = True
    run_local = os.environ['runLocally']

    if not str(run_local).upper() == 'FALSE':
        run_local_sentinel = True

    if run_local_reached:
        Config.initialize()
        if run_local_sentinel:
            app.run(host='0.0.0.0', port=int(Config.port_number), debug=True)
except ValueError as ve:
    print('')
    print('\033[94m{0}\033[0m - {1}'.format(parameter_name, str(ve)))
    print()
except KeyError as ke:
    if str(ke) == "'runLocally'":
        print()
        print('Warning: runLocally not set. To run notifications outside of')
        print('docker, do the following:')
        print()
        print('e.g. $ \033[94mrunLocally=TRUE; export runLocally\033[0m')
        print()
        run_local_sentinel = False
    else:
        print()
        print('Error: {0} is not defined.'.format(ke))
        print('Please set the variable before running python3 runserver.py')
        print()
        print('e.g. $ \033[94m{0}=xxxx; export {0}\033[0m'\
            .format(str(ke).replace("'","")))
        print()
except Exception as e:
    print(repr(e))

