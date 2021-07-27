"""
Helper functions to be used within the main module, app.py.
"""
from pathlib import Path
import sqlite3

db_path = Path.cwd().parent / ('database/storage_db.db')

# Establishes the connection to the database
def get_db_connection():
    """
    Opens a connection to the database.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# Helper functions for the bulk update
def get_categories() -> list:
    """
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
    """
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



