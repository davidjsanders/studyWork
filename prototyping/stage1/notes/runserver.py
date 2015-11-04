from flask_restful import Api
from notes import app, api
app.run(host='0.0.0.0', debug=True)
