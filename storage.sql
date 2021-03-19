DROP TABLE IF EXISTS storage;

CREATE TABLE storage (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	Category TEXT,
	Name TEXT,
	Quantity INTEGER,
	Expiry_date INTEGER,
	Deleted INTEGER
);
