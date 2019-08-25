#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request

app=Flask(__name__)
# manually create dictionary
tasks=[
    {
        'id':1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id':2,
        'title': u'Learn Python',
        'description': u'Need to Find a good Python Tutorial on the web',
        'done': False

    }
]


# ******to return all dictionary******;

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

#************ to get specific task id******************
# ***********note how to use api call in url********
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_tasks_ind(task_id):
    task=[task for task in tasks if task['id']==task_id]
# *******allow for error code***********
    if len(task)==0:
        abort(404)
    return jsonify({'tasks': task[0]})

# *******handle errors*******
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not Found'}),404)


# ***********setup a post method***********8
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
#********* error handling ensure json is posted with request and json has
# *************** a title*********
    if not request.json or not 'title' in request.json:
        abort(400)
    task={
        'id':tasks[-1]['id']+1,
        'title': request.json['title'],
        'description': request.json.get('description',""),
        'done':False
    }
    tasks.append(task)
    return jsonify({'task':task}),201

# ******** put task*************;
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task=[task for task in tasks if task['id']==task_id]
    if len(task)==0 :
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title'])!=str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title']=request.json.get('title', task[0]['title'])
    task[0]['description']=request.json.get('description', task[0]['description'])
    task[0]['done']=request.json.get('done', task[0]['done'])
    return jsonify({'task':task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id']==task_id]
    if len(task)==0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result':True})


if __name__=='__main__':
  app.run(debug=True)
