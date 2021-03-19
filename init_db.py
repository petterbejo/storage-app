import sqlite3

conn = sqlite3.connect('basement_db.db')

with open('storage.sql') as s:
    conn.executescript(s.read())

c = conn.cursor()

c.execute('INSERT INTO storage (Category, Name, Quantity, Expiry_date, Deleted) VALUES (?, ?, ?, ?, ?)',
         ('Mehl', 'Weizen VK', 4, 2109, 0)
         )

c.execute('INSERT INTO storage (Category, Name, Quantity, Expiry_date, Deleted) VALUES (?, ?, ?, ?, ?)',
         ('Mehl', 'Dinkel 630', 2, 2111, 0)
         )

c.execute('INSERT INTO storage (Category, Name, Quantity, Expiry_date, Deleted) VALUES (?, ?, ?, ?, ?)',
         ('Getranke', 'Zubrowka', 1, 0, 0)
         )

conn.commit()
conn.close()
