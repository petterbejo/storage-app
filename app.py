import sqlite3
from flask import Flask, render_template

def get_db_connection():
    conn = sqlite3.connect('basement_db.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)

@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM storage').fetchall()
    conn.close()
    return render_template('frontpage.html', storage=items)


