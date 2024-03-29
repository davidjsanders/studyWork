"""
    Application: notes
    Overivew:    A demonstration of a device, such as a smart phone, which
                 provides notifications and only changes the behaviour of the
                 notifications based on locked or unlocked status. The key
                 element of this demonstrator is to show that the device is
                 set to a priori context only.
    Purpose:     To demonstrate how a solution could be modelled by developing
                 a skeleton version of the application using any language, in
                 this case Python. The model is relatively easy to build and
                 simulation occurs through the building and executing of the
                 application modules in Docker to minimize dependency issues.
                 Python was selected for its ability to easily deliver both
                 object-oriented designs and for the RESTful extensions
                 provided by flask_restful.
    Patterns:    Larger Applications pattern from Flask website (Ronacher,
                 2013)

    App Structure
    -------------
    notesense/            - main directory
        runserver.py      - application core
    notes/notes/          - package structure
        __init__.py       - ensures Python treats directories as packages, also
                            defines key global variables app and api (Souren,
                            2015)
        main.py           - the main module of the program
        resources/        - the resources (modules) folder
            Config.py        - the Config class
            Notifications.py - the Notification, NotificationGetter, and 
                               NotificationAdder classes
            Lock.py          - the Lock and Unlock classes
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

# Run the server. host = '0.0.0.0' enables access from any endpoint (necessary
# for using with Docker), debug=True enables verbose debugging - not to be used
# in production.
app.run(host='0.0.0.0', debug=True)
