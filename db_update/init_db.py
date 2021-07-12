"""
Creates the database and stores the items in the provided CSV file in
the database.

If the database already exists, it is deleted first.
"""
import os
import sqlite3
import csv
from categories_and_csv import categories, storage_csv

# Assign database path to variable
db_path = '../database/storage_db.db'

# Delete database if exists
if os.path.exists(db_path):
    os.remove(db_path)


# Create new database
conn = sqlite3.connect(db_path)
c = conn.cursor()


# Create tables
create_items_table = """CREATE TABLE items (
                        item_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        category_id INTEGER NOT NULL,
                        article TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        expiry_date INTEGER NOT NULL
                        );"""

create_categories_table = """CREATE TABLE categories (
                             category_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                             category TEXT NOT NULL
                             );"""

c.execute(create_items_table)
c.execute(create_categories_table)



# Write your personal categories to the categories table
for cat in categories:
    c.execute('INSERT INTO categories VALUES (?, ?)', [cat[0], cat[1]])


# Write your personal storage_csv file to the database
with open(storage_csv) as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
        for cat in categories:
            if row[0] == cat[1]:
                item_cat = cat[0]
        c.execute('INSERT INTO items '
                  '(category_id, article, quantity, expiry_date) '
                  'VALUES (?, ?, ?, ?) ',
                  [item_cat, row[1], row[2], row[3]])


conn.commit()
conn.close()

