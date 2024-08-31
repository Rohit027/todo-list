from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuring SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)

# Create the database
with app.app_context():
    db.create_all()

# Routes
@app.route('/tasks', methods=['GET'])
def get_tasks():
    filter_by_completion = request.args.get('completed')
    if filter_by_completion is not None:
        tasks = Task.query.filter_by(completed=bool(int(filter_by_completion))).all()
    else:
        tasks = Task.query.all()
    return jsonify([{"id": task.id, "title": task.title, "description": task.description, "completed": task.completed} for task in tasks])

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(title=data['title'], description=data.get('description', ''))
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task created", "task": {"id": new_task.id, "title": new_task.title, "description": new_task.description, "completed": new_task.completed}})

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({"message": "Task not found"}), 404
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify({"message": "Task updated", "task": {"id": task.id, "title": task.title, "description": task.description, "completed": task.completed}})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({"message": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})

if __name__ == '__main__':
    app.run(debug=True)
