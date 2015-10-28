#!/flask/bin/python3
from flask import Flask, jsonify, abort, make_response, request, url_for
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
debug_state = False
lock_status = False #True       # The device ALWAYS starts in locked mode
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

@app.route('/lock', methods=['GET'])
def get_lock_status():
    #"""
    #http://host/lock interrogates the device and returns the locked status
    #of the device, either true or false
    #"""
    #return make_response(jsonify({'locked':lock_status}), 201)
    return make_response(jsonify({'return_state':lock_status})), 201

@app.route('/lock', methods=['PUT'])
def action_lock_device():
    global lock_status
    lock_status = True
    return make_response(jsonify({'return_state':lock_status})), 201

@app.route('/unlock/<int:pin_code>', methods=['PUT'])
def action_unlock_device(pin_code):
    response_code = 400
    global lock_status
    if (pin_code == unlock_pin):
        lock_status = False
        response_code = 201
    return make_response(jsonify({'return_state':lock_status})), response_code

@app.route('/wear', methods=['GET'])
def get_wear_status():
    global being_worn
    global being_worn_by

    response_code = 200
    response_text = being_worn_by
    if (being_worn == False):
        response_code = 200
        response_text = 'Watch is not being worn'
    return make_response(jsonify({'being_worn_by':response_text}), response_code)

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
