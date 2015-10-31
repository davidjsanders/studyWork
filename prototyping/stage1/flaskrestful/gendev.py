#!/flask/bin/python3
from flask import Flask, jsonify, abort, make_response, request, url_for
import json
import sys
#from flask.ext.httpauth import HTTPBasicAuth
#import sqlite3

# To Do
# ------

# Global variables
# ----------------
global_rules = []
global_dataitems = {}
global_action_list = {'david':'David J. Sanders'}

debug_state = True
lock_status = True       # The device ALWAYS starts in locked mode
unlock_pin = 1234        # pin code required to unlock the device
allergies = ['peanuts', 'seafood']

app = Flask(__name__)    # The applicaiton

#
# Refactored - 31 Oct 2015, DJS, 12:01
#

# ------------------------------------
# 'internal' methods
# ------------------------------------
# TO DO: Make these *really* internal only

def abort_action(abort_status):
    #TO DO: Custom stuff
    abort(abort_status)


# ------------------------------------
# Routes
# ------------------------------------

# /routes - GET
# Purpose - return routes to this devices
#
@app.route('/', methods=['GET'])
def route_routes():
    action_list = []
    # References
    # http://stackoverflow.com/questions/13317536/get-a-list-of-all-routes-defined-in-the-app
    # http://flask.pocoo.org/snippets/117/

    for route in app.url_map.iter_rules():
        options = {}
        for arg in route.arguments:
            options[arg] = '<{0}>'.format(arg)

        methods = ', '.join(route.methods)
        url = url_for(route.endpoint, _external=True, **options)
        action_list.append({'route':route.endpoint, 'methods':methods, 'url':url, 'doc':app.view_functions[route.endpoint].__doc__})

    return make_response(jsonify({'actions':action_list}), 201)


# /actions - GET
# Purpose - what actions can this device perform?
#
@app.route('/actions', methods=['GET'])
def route_actions():
    """
    route_actions() called via /actions
    returns a JSON list containing the actions that
    can be performed by this device
    """

    # Connect globals used in this method
    global global_action_list

    # Find out the method used to invoke this route
    invoke_method = request.method.upper()

    # Check if the method is supported, if not, abort 405.
    if not invoke_method in ['GET']:
        abort_action(405)

    # Check if the action list is empty, if it is, abort 404.
    if len(global_action_list) < 1:
        abort(404)

    # Return the action list
    return_response = make_response(jsonify(global_action_list), 200)

    return return_response;

# /action/<string:actionID> - GET, PUT, POST, DELETE
# Purpose - what actions can this device perform?
#
@app.route('/action/<string:action_ID>', methods=['GET', 'PUT', 'POST', 'DELETE'])
def route_action(action_ID):
    """
    get_action() called via /action/<action ID>
    Depending upon the method used to invoke this route
    either creates, reads, updates, or deletes an action
    from the device.
    """

    # Find out the method used to invoke this route
    invoke_method = request.method.upper()

    # Check if the method is supported, if not, abort 405.
    if invoke_method == 'GET':
        return action_get(action_ID)
    elif invoke_method == 'PUT':
        if not request.json:
            abort_action(400)
        return action_set(action_ID, request.json)
    else:
        abort_action(400)


# ------------------------------------
# Functions
# ------------------------------------
def action_get(action_ID):
    # Connect globals used in this method
    global global_action_list

    # Check if the action ID is nothing
    if action_ID == None or action_ID == "":
        abort_action(400)

    # Check there are actions defined
    if len(global_action_list) < 1:   # IE no actions defined, so return 404
        abort_action(404)

    # Try to get the action and return its value, otherwise return
    # the exception raised.
    try:
        return_value = {action_ID:global_action_list[action_ID]}
    except:
        return_value = {'error':str(sys.exc_info()[0])}

    return make_response(jsonify(return_value))

def action_set(action_ID, json_data):
    # Connect globals used in this method
    global global_action_list

    # Check if the action ID is nothing
    if action_ID == None or action_ID == "":
        abort_action(400)

    # Try to set the action and return its value, otherwise return
    # the exception raised.
    try:
        global_action_list[action_ID] = json_data
        return_value = {action_ID:global_action_list[action_ID]}
    except:
        return_value = {'error':str(sys.exc_info()[0])}

    return make_response(jsonify(return_value))


# Main
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=debug_state)
