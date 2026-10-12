'''from flask import Flask, render_template
app = Flask(__name__)

#static route
@app.route('/greet')
def greet():
    return "Good morning!"

#dynamic route
@app.route('/user/<username>')
def get_User(username):
    return f'Hello, {username}!'

#typed dynamic route
"""
@app.route('/price/<float:amount>')
def getBill(amount):
    return f'Total = ${amount}'
"""

#HTTP methods &render templete
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
'''
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB = 'database.db'

# ---------- DB helpers ----------
def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row   # lets us use row['col_name']
    return conn

def init_db():
    conn = get_conn()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL,
            email TEXT NOT NULL,
            age   INTEGER
        )
    ''')
    # seed a few rows only if empty
    if conn.execute('SELECT COUNT(*) FROM users').fetchone()[0] == 0:
        conn.executemany(
            'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
            [
                ('Ravi',   'ravi@example.com',   25),
                ('Priya',  'priya@example.com',  30),
                ('Arjun',  'arjun@example.com',  22),
            ]
        )
    conn.commit()
    conn.close()

init_db()

# ---------- Routes ----------

# 1. Show all users (READ)
@app.route('/')
def users():
    conn = get_conn()
    rows = conn.execute('SELECT * FROM users ORDER BY id').fetchall()
    conn.close()

    # rows is a list of sqlite3.Row objects
    return render_template('users.html', users=rows)


# 2. Show add-user form (GET)
@app.route('/add')
def add_form():
    return render_template('add_user.html')


# 3. Handle add-user submit (CREATE)
@app.route('/add', methods=['POST'])
def add_user():
    name  = request.form['name']
    email = request.form['email']
    age   = request.form['age']

    conn = get_conn()
    conn.execute(
        'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
        (name, email, age)
    )
    conn.commit()
    conn.close()

    # After saving, redirect back to list (Post/Redirect/Get pattern)
    return redirect(url_for('users'))


if __name__ == '__main__':
    app.run(debug=True)
