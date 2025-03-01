from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    workspace = sqlite3.connect('todo.db')
    c = workspace.cursor()

    c.execute('SELECT * FROM tasks')

    tasks = c.fetchall()
    workspace.close()
    
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add():
    d = request.form['description']
    print(type(d), d)

    workspace = sqlite3.connect('todo.db')
    c = workspace.cursor()

    c.execute('INSERT INTO tasks (description) VALUES (?)', (d,))

    workspace.commit()
    workspace.close()
    
    return redirect(url_for('index'))


@app.route('/complete/<int:task_id>')
def complete(task_id):
    workspace = sqlite3.connect('todo.db')
    c = workspace.cursor()

    c.execute('UPDATE tasks SET done = 1 WHERE id = ?', (task_id,))

    workspace.commit()
    workspace.close()
    
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete(task_id):
    workspace = sqlite3.connect('todo.db')
    c = workspace.cursor()

    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))

    workspace.commit()
    workspace.close()
    
    return redirect(url_for('index'))


def init_database():
    workspace = sqlite3.connect('todo.db')
    c = workspace.cursor()

    c.execute(
        '''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL, done BOOLEAN NOT NULL DEFAULT 0)''')

    workspace.commit()
    workspace.close()


init_database()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
