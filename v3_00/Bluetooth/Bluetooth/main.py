from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Bluetooth import app, api

from Bluetooth_Config_Boundary import main

# Reference: Adamo, D. [2015], 'Handling CORS Requests in Flask(-RESTful) APIs'
# [ONLINE]. Available at: http://www.davidadamojr.com/handling-cors-requests-in-flask-restful-apis/
# (Accessed: 08 March 2016)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
        'Origin, X-Requested-With, Content-Type, Authorization, Accept')
    response.headers.add('Access-Control-Allow-Methods',
        'GET,PUT,POST,OPTIONS,HEAD,DELETE')
    return response


