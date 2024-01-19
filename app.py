from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks_db = []
taks_id_control = 1

@app.route('/tasks', methods=['GET'])
def tasks():
  task_list = [task.to_dict() for task in tasks_db]

  output = {
    'tasks' : task_list,
    'total_tasks': len(task_list)
  }

  return jsonify(output)

@app.route('/tasks', methods=['POST'])
def create_task():
  global taks_id_control
  data = request.get_json()
  new_task = Task(id=taks_id_control, title=data['title'], description=data.get('description', ''))
  taks_id_control += 1
  tasks_db.append(new_task)
  
  return jsonify({
    'message': 'New task created.', 
    "id": new_task.id
  })

@app.route('/tasks/<int:id>', methods=['GET'])
def show(id):
  task = set_task(id)
  
  if not task:
    return jsonify({'message': 'Task not found.'}), 404

  return jsonify(task.to_dict())

@app.route('/tasks/<int:id>', methods=['PUT'])
def update(id):
  task = set_task(id)

  if not task:
    return jsonify({'message': 'Task not found.'}), 404

  data = request.get_json()
  
  task.title = data['title']
  task.description = data['description'] or ''
  task.completed = data['completed']

  return jsonify({
      "message": "Task updated.",
      "id": task.id,
      "title": task.title,
      "description": task.description,
      "completed": task.completed
    })

@app.route('/tasks/<int:id>', methods=['DELETE'])
def destroy(id):
  task = set_task(id)

  if not task:
    return jsonify({'message': 'Task not found.'}), 404
  
  tasks_db.remove(task)
  return jsonify({'message': 'Task deleted.'})


def set_task(id):
  for t in tasks_db:
      if t.id == id:
          return t

  return None


if __name__ == '__main__':
  app.run(debug=True)
