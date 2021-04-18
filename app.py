import sqlite3
from flask import Flask, render_template, request, url_for, redirect

def get_db_connection():
    """
    Opens a connection to the database.
    """
    conn = sqlite3.connect('my_db.db')
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


@app.route('/<int:id>/remove', methods=('GET', 'POST'))
def remove_item(id):
    conn = get_db_connection()
    conn.execute('UPDATE storage SET Quantity = Quantity - 1 WHERE id = ?', (id,))  
    conn.commit()
    conn.close()
    return redirect(url_for('index')) 


@app.route('/<int:id>/add', methods=('GET', 'POST'))
def add_item(id):
    conn = get_db_connection()
    conn.execute('UPDATE storage SET Quantity = Quantity + 1 WHERE id = ?', (id,))  
    conn.commit()
    conn.close()
    return redirect(url_for('index')) 
