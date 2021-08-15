from pathlib import Path

from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect

from helper_functions import get_db_connection
from helper_functions import get_categories
from helper_functions import assign_category_id
from helper_functions import csv_converter
from helper_functions import already_in_storage
from helper_functions import get_item_id

db_path = Path.cwd().parent / ('database/storage_db.db')

app = Flask(__name__)


@app.route('/')
def index():
    """ Views the front page.
    """
    conn = get_db_connection()
    items = conn.execute(
        'SELECT item_id, categories.category, article, quantity, expiry_date '
        'FROM items '
        'INNER JOIN categories '
        'ON items.category_id=categories.category_id '
        'ORDER BY category'
         ).fetchall()
    conn.close()
    num_articles = len(items)
    return render_template('frontpage.html',
                           storage=items, num_articles=num_articles)


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
    """ Lets the user view and select all available categories.
    """
    conn = get_db_connection()
    items = conn.execute(
        'SELECT * '
        'FROM categories '
        'ORDER BY category'
    ).fetchall()
    conn.close()
    return render_template('categoryview.html', categories=items)


@app.route('/<int:category_id>/category_view')
def single_category(category_id):
    """ Views items of a single category.
    """
    conn = get_db_connection()
    items = conn.execute(
        'SELECT item_id, categories.category, article, quantity, '
        'expiry_date, categories.category_id '
        'FROM items '
        'INNER JOIN categories '
        'ON items.category_id=categories.category_id '
        'WHERE categories.category_id = ? '
        'ORDER BY article', (category_id,)
    ).fetchall()
    conn.close()
    return render_template('singlecategory.html', category=items)


@app.route('/bulk_update')
def bulk_update_page():
    """ Returns the page to select and upload a CSV file.
    """
    return render_template('bulkupdate.html')


@app.route('/run_bulk_update', methods=('GET', 'POST'))
def run_bulk_update():
    """ Write new content to the database from uploaded CSV file.

    Takes the uploaded file, writes each row as a list within the final
    list, then writes each of these lists to the database.

    The function does not use the CSV module because of decoding issues.
    """
    converted_file = csv_converter('file')
    categories = get_categories()
    conn = get_db_connection()
    omitted = []
    updated = []
    for row in converted_file:
        if row[0] in categories:
            if already_in_storage(row):
                item_id = get_item_id(row)
                conn.execute('UPDATE items '
                      'SET Quantity = Quantity + ? '
                      'WHERE item_id = ? ', (row[2], item_id, ))
                updated.append([row])
            else:
                conn.execute('INSERT INTO items '
                      '(category_id, article, quantity, expiry_date) '
                      'VALUES (?, ?, ?, ?) ',
                      [assign_category_id(row[0]), row[1], row[2], row[3]])

        else:
            omitted.append([row])
    conn.commit()
    conn.close()
    return render_template('updatecompleted.html', omitted=omitted, updated=updated)