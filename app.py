from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

def setUpDatabaseConnection(app):
    DATABASE_URL = os.getenv('DATABASE_URL')
    if DATABASE_URL == None:
        raise Exception("Database is required")
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    db = SQLAlchemy(app)
    return db

def createTodoModel(db):
    class Todo(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        content = db.Column(db.String(200), nullable=False)
        completed = db.Column(db.Integer, default=0)
        created_at = db.Column(db.DateTime, default=datetime.now())

        def __repr__(self):
            return '<Task %r>' % self.id
    return Todo


def registerRoutes(db, Todo):
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



    @app.route('/pricing')
    def pricing():
        return render_template('pricing.html', tier1Price=3000, tier2Price=5000)


if __name__ == "__main__":
    print(':::CONNECTING TO DATABASE...')
    db = setUpDatabaseConnection(app)
    print(':::CONNECTED TO DATABASE SUCCESSFULLY')
    
    Todo = createTodoModel(db)

    print(':::RUNNING MIGRATION...')
    db.create_all()
    print(':::MIGRATION COMPLETED SUCCESSFULLY')

    registerRoutes(db, Todo)
    app.run(debug=True)
