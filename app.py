import sqlite3
from flask import Flask, render_template, request, url_for, redirect

def get_db_connection():
    """
    Opens a connection to the database.
    """
    conn = sqlite3.connect('basement_db.db')
    conn.row_factory = sqlite3.Row
    return conn


# Add function to remove item from db here

# Add function to add item to db here

app = Flask(__name__)

@app.route('/')
def index():
    """
    Views the front page.
    """
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM storage').fetchall()
    conn.close()
    return render_template('frontpage.html', storage=items)


@app.route('/test')
def test():
    return "Hello there, this is just a test."


@app.route('/<int:id>', methods=('GET', 'POST'))
def update(id):
    conn = get_db_connection()
    # conn.execute(' FROM storage WHERE id = ?', (id,))  
    conn.close
    return redirect(url_for('test'))
