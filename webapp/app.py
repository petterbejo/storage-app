from pathlib import Path
from flask import Flask, render_template, request, url_for, redirect
from helper_functions import get_db_connection, get_categories

db_path = Path.cwd().parent / ('database/storage_db.db')

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


@app.route('/<int:id>/<page>/<int:category>/remove', methods=('GET', 'POST'))
@app.route('/<int:id>/<page>/remove', methods=('GET', 'POST'))
def remove_item(id, page, category=None):
    conn = get_db_connection()
    conn.execute('UPDATE items SET Quantity = Quantity - 1 WHERE item_id = ?', (id,))
    conn.commit()
    conn.close()
    if category:
        return redirect(url_for('single_category', category_id=category))
    return redirect(url_for(page))


@app.route('/<int:id>/<page>/<int:category>/add', methods=('GET', 'POST'))
@app.route('/<int:id>/<page>/add', methods=('GET', 'POST'))
def add_item(id, page, category=None):
    conn = get_db_connection()
    conn.execute('UPDATE items SET Quantity = Quantity + 1 WHERE item_id = ?', (id,))
    conn.commit()
    conn.close()
    if category:
        return redirect(url_for('single_category', category_id=category))
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


@app.route('/<int:category_id>/category_view')
def single_category(category_id):
    """
    Views items of a single category.
    """
    conn = get_db_connection()
    items = conn.execute(
        'SELECT item_id, categories.category, article, quantity, '
        'expiry_date, categories.category_id '
        'FROM items '
        'INNER JOIN categories '
        'ON items.category_id=categories.category_id '
        'WHERE categories.category_id = ?', (category_id,)
    ).fetchall()
    conn.close()
    return render_template('singlecategory.html', category=items)


@app.route('/bulk_update')
def bulk_update():
    """
    Reads an uploaded CSV file and appends its content to the database.
    """
    return render_template('bulkupdate.html')


@app.route('/update_completed', methods=('GET', 'POST'))
def update_completed():
    """
    Takes the uploaded file, writes each row as a list within the final
    list, then writes each of these lists to the database.

    The function does not use the CSV module because of decoding issues.
    """
    file = request.files['file'].read()
    raw = file.splitlines()
    final = []
    for element in raw:
        new_ele = element.decode()
        final.append(new_ele.split(','))
    conn = get_db_connection()
    for row in final:
        conn.execute('INSERT INTO items '
                  '(category_id, article, quantity, expiry_date) '
                  'VALUES (?, ?, ?, ?) ',
                  [2, row[1], row[2], row[3]])
    conn.commit()
    conn.close()
    return f'Uploaded file is a {final}, oh yeah'