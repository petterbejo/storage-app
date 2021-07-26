"""
Helper functions to run a bulk update with a CSV file.
"""
from pathlib import Path
import sqlite3

db_path = Path.cwd().parent / ('database/storage_db.db')

def get_db_connection():
    """
    Opens a connection to the database.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_categories():
    conn = get_db_connection()
    categories = conn.execute(
        'SELECT category '
        'FROM categories'
        ).fetchall()
    formatted = [category[0] for category in categories]
    return formatted

