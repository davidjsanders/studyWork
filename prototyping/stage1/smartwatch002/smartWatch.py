#!/flask/bin/python3
from flask import Flask, jsonify, abort, make_response, request, url_for
import json
import sys
#from flask.ext.httpauth import HTTPBasicAuth
#import sqlite3

# To Do
# ------
# 1. Add context on Network - EMS available when watch worn and no network?
# 2. Break glass
# 3. GPS tracking / geo location
# 4. Activity based - because I'm out running?
# 5. Avoiding situations where it can't be feasible for EMS button - driving, etc.

# Global variables
# ----------------
global_rules = []
global_dataitems = {}
global_action_list = {}
debug_state = True
lock_status = True       # The device ALWAYS starts in locked mode
unlock_pin = 1234        # pin code required to unlock the device
allergies = ['peanuts', 'seafood']
medical_bracelet = {'medical_bracelet': \
        {'name':'John Doe', \
         'age':51, \
         'allergies':allergies, \
         'emergency_contact':'+1 555 755 5757' \
        } \
    }
medical_ems = {'ems': \
        {'bracelet':medical_bracelet, \
         'patient_id':'12XXA8990', \
         'fullname':'John Joseph Doe', \
         'address':['22 Acadia Av E.','Anytown', 'ON', 'H0H0H0', 'CANADA'], \
         'blood':'AB+' \
        } \
    }
being_worn = False # You have to put the watch on
being_worn_by = "" # who is wearing the watch - default no one

app = Flask(__name__)    # The applicaiton

def build_response(data, code=200):
    response_data = make_response(jsonify(data), code)
    return response_data

def not_ready():
    response_data = make_response(jsonify({"status":"Still a work in progress - i.e. to do "}), 400)
    return response_data 

@app.route('/actions', methods=['GET'])
def get_action_list():
    return make_response(jsonify(global_action_list), 200)

@app.route('/action/<string:item>', methods=['GET'])
def get_action(item):
    response_data = ''

    try:
        response_data = make_response(jsonify({'action':global_action_list[item]}), 200)
    except KeyError:
        abort(404)
    except:
        e = sys.exc_info()[0]
        return make_response(jsonify({'error':str(e)}), 400)
#        abort(404)

    return response_data

#    return not_ready();

@app.route('/action/<string:item>', methods=['PUT'])
def set_action(item):
#    if not request.json:
#        abort(400)

    global_action_list[item] = item

    return make_response(jsonify(global_action_list), 200)



@app.route('/data/<string:item>', methods=['GET'])
def get_data(item):
#    global global_dataitems

    if len(global_dataitems) == 0:
        abort(404) 

    dataitem = None
    try:
        dataitem = global_dataitems[item]
    except:
        abort(404)

    return jsonify({'data':dataitem}), 200

@app.route('/data/<string:item>/<int:key>', methods=['GET'])
def get_data_json(item, key):
    if len(global_dataitems) == 0:
        abort(404) 

    dataitem = None
    try:
        dataitem = global_dataitems[item]
    except:
        abort(404)

    if not type(dataitem) is list:
        return jsonify({'error':'data item is not a list'}), 400

    try:
        dataitem = dataitem[key]
    except:
        abort(404)

    return jsonify({'data':dataitem}), 200


@app.route('/data/<string:item>', methods=['PUT'])
def set_data_json(item):
    if not request.json:
        abort(400)

    global_dataitems[item] = request.json
    return get_data(item)

@app.route('/custom', methods=['GET','PUT','POST','DELETE'])
def action_custom():
    if not request.json \
    or not 'action' in request.json:
        abort(400)

    method = ""
    if 'method' not in request.json:
        method = request.form.get('_method', '').upper()
    else:
        method = request.json['method'].upper()

    if method not in ['GET','PUT','POST','DELETE']:
        return_string = "Method '{}' not recognized.".format(method)
        return jsonify({'error':return_string}), 400

    action = request.json['action']
    items = []

    for item in request.json:
        if item not in 'action' \
        and item not in 'method':
            items.append({item:request.json[item]})

    return_dict = {
         "action":action,
         "method":method,
         "parameters":items
        }

    return jsonify(return_dict), 200

@app.route('/rule/<string:rule>', methods=['POST'])
def action_add_rule(rule):
    if not request.json:
        abort(400)

    elements = []
    for element in request.json:
        if element != 'methods':
            elements.append({'parameter':element, 'datatype':request.json[element]})

    if 'methods' in request.json:
        new_rule = {'rule':rule, 'parameters':elements, 'methods':request.json['methods']}
    else:
        new_rule = {'rule':rule, 'parameters':elements, 'methods':['GET']}

    global_rules.append(new_rule)
    return make_response(jsonify({'new rule':new_rule}), 200)
    #return make_response(jsonify({'new rule':'success'}), 200)

@app.route('/rules', methods=['GET'])
def get_rules():
    return make_response(jsonify({'rules':global_rules}), 200)

@app.route('/', methods=['GET'])
def get_actions():
    action_list = []
    # References
    # http://stackoverflow.com/questions/13317536/get-a-list-of-all-routes-defined-in-the-app
    # http://flask.pocoo.org/snippets/117/

    for route in app.url_map.iter_rules():
        options = {}
        for arg in route.arguments:
            options[arg] = '[{0}]'.format(arg)

        methods = ', '.join(route.methods)
        #url = url_for(route.endpoint, **options)
        action_list.append({'route':route.endpoint, 'methods':methods})

    return make_response(jsonify({'actions':action_list}), 201)

@app.route('/lock', methods=['GET'])
def get_lock_status():
    # http://host/lock interrogates the device and returns the locked status
    # of the device, either true or false

    # return make_response(jsonify({'locked':lock_status}), 201)
    return build_response( \
        data={'return_state':lock_status}, \
        code=201 \
    )

@app.route('/lock', methods=['PUT'])
def action_lock_device():
    global lock_status
    lock_status = True
    return get_lock_status()

@app.route('/unlock/<int:pin_code>', methods=['PUT'])
def action_unlock_device(pin_code):
    response_code = 400
    global lock_status

    if (pin_code == unlock_pin):
        lock_status = False
        response_code = 201
    return build_response(data={'return_state':lock_status}, code=response_code)

@app.route('/wear', methods=['GET'])
def get_wear_status():
    global being_worn
    global being_worn_by

    response_code = 200
    response_text = being_worn_by
    if (being_worn == False):
        response_code = 200
        response_text = 'Watch is not being worn'
    return build_response(data={'being_worn_by':response_text}, code=response_code)

@app.route('/wear/<string:wearer_name>', methods=['PUT'])
def action_wear_smartwatch(wearer_name):
    global being_worn
    global being_worn_by

    response_code = 201
    if (being_worn == True):
        return make_response(jsonify({'return_state':False, 'being_worn_by':being_worn_by}), 403)
    if (wearer_name == None):
        response_code = 400
    being_worn_by = wearer_name
    being_worn = True
    return make_response(jsonify({'return_state':True, 'being_worn_by':being_worn_by}), response_code)

@app.route('/takeoff', methods=['PUT'])
def action_takeoff_smartwatch():
    global being_worn
    global being_worn_by
    if (being_worn == False):
        return make_response(jsonify({'return_state':False, 'being_worn_by':'no one'}), 204)
    being_worn_by = ""
    being_worn = False
    return make_response(jsonify({'return_state':True, 'being_worn_by':'no one'}), 200)

@app.route('/healthdata', methods=['GET'])
def get_health_data():
    global lock_status

    health_data = {'health':{'steps':1234, 'kilometres':12.3, 'pulse':62, 'bpi':'70/110'}}
    if (lock_status == True):
        return make_response(jsonify({'error':'device locked'})), 403

    return make_response(jsonify(health_data)), 200

@app.route('/medical_bracelet', methods=['GET'])
def get_medical_bracelet():
    global being_worn

    if (being_worn == False):
        return make_response(jsonify({'error':'device not being worn'}), 403)
    return make_response(jsonify(medical_bracelet)), 200

@app.route('/medical_ems/<string:unique_id>', methods=['GET'])
def get_medical_ems(unique_id):
    global being_worn

    if (being_worn == False):
        return make_response(jsonify({'error':'device not being worn'}), 403)
    return make_response(jsonify(medical_ems), 200)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=debug_state)
