"""
Creates the database and stores the items in the provided CSV file in the database.
"""
import sqlite3
import csv

# create db
# create tables
# insert items from csv
# close connection


# create db
conn = sqlite3.connect('storage_db.db')
c = conn.cursor()

# create tables
create_items_table = """DROP TABLE items
                        CREATE TABLE items (
                        item_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        category_id INTEGER NOT NULL,
                        article TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        expiry_date INTEGER NOT NULL
                        );"""

create_categories_table = """DROP TABLE categories
                             CREATE TABLE categories (
                             category_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                             category TEXT NOT NULL,
                             );"""



# Provide the path of your CSV here (as a string):
storage_csv = 'in_storage_test.csv'

with open(storage_csv) as f:



conn.commit()
conn.close()
