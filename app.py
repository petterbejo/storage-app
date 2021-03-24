import sqlite3
from flask import Flask, render_template

def get_db_connection():
    """
    Opens a connection to the database.
    """
    conn = sqlite3.connect('basement_db.db')
    conn.row_factory = sqlite3.Row
    return conn


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


