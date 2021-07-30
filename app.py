from flask import Flask, render_template, request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv('APP_DATABASE_URL')
PORT = os.getenv('PORT')

if DATABASE_URL == None:
    raise Exception("Database is required")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Task %r>' % self.id

db.create_all()

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        taskContent = request.form['content']
        newTask = Todo(content=taskContent)

        try:
            db.session.add(newTask)
            db.session.commit()
            return redirect('/')
        except:
            return 'The was issue adding task'
    else:
        tasks = Todo.query.order_by(Todo.created_at).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def deleteTask(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Failed to delete task'



@app.route('/update/<int:id>', methods=['GET', 'POST'])
def updateTask(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == 'GET':
        return render_template('update.html', task=task_to_update)
    else:
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Failed to update task'

@app.route('/healthcheck')
def healthcheck():
    return 'Application works!'

@app.route('/pricing')
def pricing():
    return render_template('pricing.html', tier1Price=3000, tier2Price=5000)

@app.route('/jokes', methods=['GET'])
def hobbies():
    try:
        response = requests.get('https://nonsense.com')
        resp = Response(response, status = 200, headers = { 'Content-Type': 'application/json' })
        return resp
    except Exception as err:
        print(':::: FAILED TO FETCH JOKES ::::', str(err))
        response = { "status": 'error', "message": "Failed to fetch jokes", "code": 400 }
        return Response(json.dumps(response), 400, { 'Content-Type': 'application/json' })
    

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)
