"""
Creates the database and stores the items in the provided CSV file in the database.
"""


import sqlite3
import pandas as pd


conn = sqlite3.connect('my_db.db')
c = conn.cursor()

# Provide the path of your CSV here (as a string):
my_csv = ' '

read_storage = pd.read_csv(my_csv))
read_storage.to_sql('storage', conn, if_exists='replace', index=False)

conn.commit()
conn.close()
