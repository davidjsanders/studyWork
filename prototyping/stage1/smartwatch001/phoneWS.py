# #!/flask/bin/python3
from flask import Flask, jsonify, abort, make_response, request, url_for
#from flask.ext.httpauth import HTTPBasicAuth
#import sqlite3
#auth = HTTPBasicAuth()
database = '/scratch/tasks.db'

#@auth.get_password
#def get_password(username):
#    if username == 'david':
#        return 'sanders'
#    return None

#@auth.error_handler
#def unauthorized():
#    return make_response(jsonify({'error':'Unauthorized access'}), 401)

app = Flask(__name__)

def make_hyperlink(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external= True)
        else:
            new_task[field] = task[field]
    return new_task

#@app.errorhandler(404)
#def not_found(error):
#    return make_response(jsonify({'error':'Not found.'}),404)

@app.route('/actions', methods=['GET'])
def whatIdo():
    return jsonify( \
        {'actions':{'action1':'do this', 'action2':'do that'}} \
        ), 201

#@app.route('/tasks', methods=['POST'])
#def create_task():
#    if not request.json \
#    or not 'title' in request.json \
#    or not 'description' in request.json \
#    or not 'done' in request.json:
#        abort(400)
#    if request.json['title'] == '':
#        abort(400)
#    connection = sqlite3.connect(database)
#    insert_statement = 'insert into tasks (title, description, done) values (?, ?, ?)'
#    with connection:
#        cursor = connection.cursor()
#        cursor.execute(insert_statement, \
#            (request.json['title'], \
#             request.json['description'], \
#             request.json['done']))
#    return get_tasks(), 201
#    return jsonify({'task': newtask}), 201

#@app.route('/tasks/<int:task_id>', methods=['PUT'])
#def update_task(task_id):
#    if not request.json:
#        abort(400)
#
#    task_results = []
#    for data_row in loadData(task_id):
#        task_results.append(data_row)
#
#    if len(task_results) < 1:
#        abort(404)
#
#    connection = sqlite3.connect(database)
#
#    if 'title' in request.json:
#        title = request.json['title']
#    else:
#        title = task_results[0]['title']
#
#    if 'description' in request.json:
#        description = request.json['description']
#    else:
#        description = task_results[0]['description']
#
#    if 'done' in request.json:
#        done = request.json['done']
#    else:
#        done = task_results[0]['done']
#
#    with connection:
#        cursor = connection.cursor()
#        cursor.execute("update tasks set title = ?, description = ?, done = ? where id = ?", \
#             (title, description, done, task_id))
#    return get_task(task_id)
##    return jsonify({'task': task[0]})

#@app.route('/tasks/<int:task_id>', methods=['DELETE'])
#def delete_task(task_id):
#
#    task_results = []
#    for data_row in loadData(task_id):
#        task_results.append(data_row)
#
#    if len(task_results) < 1:
#        abort(404)
#
#    connection = sqlite3.connect(database)
#
#    with connection:
#        cursor = connection.cursor()
#        cursor.execute("delete from tasks where id = ?", \
#             (task_id,))
#
#    return jsonify({'result': True})

#@app.route('/tasks', methods=['GET'])
#def get_tasks():
#    mytasks = []
#    for datarow in loadData():
#        mytasks.append(datarow)
#    return jsonify({'tasks': [make_hyperlink(task) for task in mytasks]})

#@app.route('/tasks/<int:task_id>', methods=['GET'])
#@auth.login_required
#def get_task(task_id):
#    task_results = []
#    for data_row in loadData(task_id):
#        task_results.append(data_row)
#    if len(task_results) < 1:
#        abort(404)
#    return jsonify({'task': [make_hyperlink(task) for task in task_results]})
#    return jsonify({'task':task_results})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
