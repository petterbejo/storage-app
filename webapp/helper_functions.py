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
        converted.append(new_ele.split(','))
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

    # iterate over this object, return True if match
    # return False if finishes without match
    pass