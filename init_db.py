import sqlite3
import pandas as pd


conn = sqlite3.connect('basement_db.db')
c = conn.cursor()


read_storage = pd.read_csv('/home/pbj/Documents/projects/storage-app/in_storage_210319.csv')
read_storage.to_sql('storage', conn, if_exists='replace', index=False)






conn.commit()
conn.close()
