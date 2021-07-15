from pathlib import Path
import sqlite3
from flask import Flask, render_template, request, url_for, redirect

db_path = Path.cwd().parent / ('database/storage_db.db')


def get_db_connection():
    """
    Opens a connection to the database.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)


@app.route('/')
def index():
    """
    Views the front page.
    """
    conn = get_db_connection()
    items = conn.execute(
        'SELECT item_id, categories.category, article, quantity, expiry_date '
        'FROM items '
        'INNER JOIN categories '
        'ON items.category_id=categories.category_id'
         ).fetchall()
    conn.close()
    return render_template('frontpage.html', storage=items)


@app.route('/<int:id>/remove', methods=('GET', 'POST'))
def remove_item(id, page='index'):
    conn = get_db_connection()
    conn.execute('UPDATE items SET Quantity = Quantity - 1 WHERE item_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for(page))


@app.route('/<int:id>/add', methods=('GET', 'POST'))
def add_item(id, page='index'):
    conn = get_db_connection()
    conn.execute('UPDATE items SET Quantity = Quantity + 1 WHERE item_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for(page))


@app.route('/categories')
def category_view():
    """
    Lets the user view and select all available categories.
    """
    conn = get_db_connection()
    items = conn.execute(
        'SELECT * '
        'FROM categories'
    ).fetchall()
    conn.close()
    return render_template('categoryview.html', categories=items)


@app.route('/<int:id>/category_view')
def single_category(id):
    """
    Views items of a single category.
    """
    conn = get_db_connection()
    items = conn.execute(
        'SELECT item_id, categories.category, article, quantity, expiry_date '
        'FROM items '
        'INNER JOIN categories '
        'ON items.category_id=categories.category_id '
        'WHERE categories.category_id = ?', (id,)
    ).fetchall()
    conn.close()
    return render_template('singlecategory.html', category=items)


