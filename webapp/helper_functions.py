"""
Helper functions to be used within the main module, app.py.
"""
from pathlib import Path
import sqlite3

from flask import request

db_path = Path.cwd().parent / ('database/storage_db.db')

# Establishes the connection to the database
def get_db_connection():
    """ Opens a connection to the database.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# Helper functions for the bulk update
def csv_converter(file) -> list:
    """ Converts CSV file to list of lists.

    Takes the uploaded CSV file and returns a list of lists containing
    each article with its properties (category, quantity, expiry date).
    """
    raw = request.files[file].read().splitlines()
    converted = []
    for element in raw:
        new_ele = element.decode()
        converted.append(new_ele.split(';'))
    return converted

def get_categories() -> list:
    """ Return the category names.

    Returns the category names in order to check if the category of the
    CSV file's article already exists in the database.
    """
    conn = get_db_connection()
    categories = conn.execute(
        'SELECT category '
        'FROM categories'
        ).fetchall()
    formatted = [category[0] for category in categories]
    conn.close()
    return formatted


def assign_category_id(category_name):
    """ Assign the correct category ID to an article.

    Substitutes an article's category name with the appropriate
    category ID.
    """
    conn = get_db_connection()
    category_id = conn.execute(
        'SELECT category_id '
        'FROM categories '
        'WHERE category = ?', (category_name,)
        ).fetchone()
    conn.close()
    return category_id[0]


def already_in_storage(row) -> bool:
    """Checks if an item is already in storage.

    Checks if the item is already in storage in order to determine
    whether we have to update the quantity of an existing item or
    insert a new item.

    Note that if an item is already in the database, but with a
    different expiry date, the item will be written as a new item.
    """
    conn = get_db_connection()
    in_storage_now = conn.execute(
        'SELECT article, expiry_date '
        'FROM items '
         ).fetchall()
    conn.close()
    for item in in_storage_now:
        if str(item[0]) == str(row[1]) and str(item[1]) == str(row[3]):
            return True
    return False


def get_item_id(row) -> int:
    """Returns the primary key of an existing item.

    Takes a row of the uploaded CSV file as an argument. The row must
    be of an item that has been confirmed to be in storage already.

    The function then compares the row to the content of the database
    and returns the primary key, item_id, of the item."""
    conn = get_db_connection()
    in_storage_now = conn.execute(
        'SELECT item_id, article, expiry_date '
        'FROM items '
        ).fetchall()
    conn.close()
    for item in in_storage_now:
        if str(item[1]) == str(row[1]) and str(item[2]) == str(row[3]):
            return item[0]


def categories_to_list(file) -> list:
    raw = request.form[file]
    return raw.split(', ')


