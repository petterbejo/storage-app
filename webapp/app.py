"""Main script for the app"""

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
from helper_functions import categories_to_list

app = Flask(__name__)


@app.route('/')
def index():
    """ Views the front page.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT 
            item_id, 
            categories.category, 
            article, 
            quantity, 
            expiry_date 
        FROM items 
        INNER JOIN categories 
        ON items.category_id = categories.category_id 
        ORDER BY 
            category,
            article""")
    items = cur.fetchall()
    cur.close()
    conn.close()
    num_articles = len(items)
    return render_template('frontpage.html',
                           storage=items, num_articles=num_articles)


@app.route('/<int:id>/<page>/<int:category>/remove', methods=('GET', 'POST'))
@app.route('/<int:id>/<page>/remove', methods=('GET', 'POST'))
def remove_item(id, page, category=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """UPDATE items 
           SET Quantity = Quantity - 1 
           WHERE item_id = %s""",
        (id,))
    conn.commit()
    cur.close()
    conn.close()
    if category:
        return redirect(url_for('single_category', category_id=category))
    return redirect(url_for(page))


@app.route('/<int:id>/<page>/<int:category>/add', methods=('GET', 'POST'))
@app.route('/<int:id>/<page>/add', methods=('GET', 'POST'))
def add_item(id, page, category=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """UPDATE items 
           SET Quantity = Quantity + 1 
           WHERE item_id = %s""",
        (id,))
    conn.commit()
    cur.close()
    conn.close()
    if category:
        return redirect(url_for('single_category', category_id=category))
    return redirect(url_for(page))


@app.route('/categories')
def category_view():
    """ Lets the user view and select all available categories.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT 
                DISTINCT ON (category) category,
                category_id 
           FROM categories 
           ORDER BY category;""")
    items = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('categoryview.html', categories=items)


@app.route('/<int:category_id>/category_view')
def single_category(category_id):
    """ Views items of a single category.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT 
                item_id, 
                categories.category, 
                article, 
                quantity,
                expiry_date, 
                categories.category_id 
           FROM items 
           INNER JOIN categories 
           ON items.category_id=categories.category_id 
           WHERE categories.category_id = %s
           ORDER BY article""",
        (category_id,))
    items = cur.fetchall()
    cur.close()
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
    c = conn.cursor()
    omitted = []
    updated = []
    for row in converted_file:
        if row[0] in categories:
            if already_in_storage(row):
                item_id = get_item_id(row)
                c.execute('UPDATE items '
                      'SET Quantity = Quantity + %s '
                      'WHERE item_id = (%s) ', (row[2], item_id, ))
                updated.append([row])
            else:
                c.execute(
                    """INSERT INTO items 
                                    (category_id, 
                                    article, 
                                    quantity, 
                                    expiry_date) 
                        VALUES (%s, %s, %s, %s) """,
                    [assign_category_id(
                        row[0]),
                        row[1],
                        row[2],
                        row[3]])

        else:
            omitted.append([row])
    conn.commit()
    conn.close()
    return render_template('updatecompleted.html', omitted=omitted, updated=updated)


@app.route('/setup_database')
def setup_database():
    """Returns the first page of the DB setup process"""
    return render_template('setup_db.html')

@app.route('/confirm_setup')
def confirm_setup():
    """Returns the second page of the DB setup process.

    Clicking the button on the page sets off the setup process.
    """
    return render_template('confirm_setup.html')

@app.route('/run_db_setup')
def run_db_setup():
    """Runs the DB setup process.

    The setup process is intended to be run only at the initial setup
    of the app - running this process when the tables already exist
    will result in an error. """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS items 
                    (item_id SERIAL PRIMARY KEY,
                     category_id INTEGER NOT NULL,
                     article TEXT NOT NULL,
                     quantity INTEGER NOT NULL,
                     expiry_date INTEGER NOT NULL );""")
    cur.execute(
        """CREATE TABLE IF NOT EXISTS categories 
                    (category_id SERIAL PRIMARY KEY,
                     category TEXT NOT NULL );""")
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('create_categories'))


@app.route('/create_categories')
def create_categories():
    """Returns the page to add categories."""
    return render_template('create_categories.html')


@app.route('/run_categories_insert', methods=('GET', 'POST'))
def run_categories_insert():
    """Inserts the categories added by the user into the table."""
    categories = categories_to_list('categories')
    conn = get_db_connection()
    cur = conn.cursor()
    for category in categories:
        cur.execute('INSERT INTO categories (category) VALUES (%s);', (category,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('confirm_categories'))


@app.route('/confirm_categories')
def confirm_categories():
    return render_template('confirm_categories.html')


@app.route('/export_view')
def export_view():
    """ Views the export page that allows copy-pasting all DB content"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT 
            item_id, 
            categories.category, 
            article, 
            quantity, 
            expiry_date 
           FROM items 
           INNER JOIN categories 
           ON items.category_id=categories.category_id 
           ORDER BY category""")
    items = cur.fetchall()
    cur.close()
    conn.close()
    num_articles = len(items)
    return render_template('export_view.html',
                           storage=items, num_articles=num_articles)
