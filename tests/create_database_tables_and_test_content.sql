CREATE TABLE IF NOT EXISTS items (
    item_id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL,
    article TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    expiry_date INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY,
    category TEXT NOT NULL
);

INSERT INTO categories (category_id, category)
VALUES
    (1, 'pasta'),
    (2, 'oil');

INSERT INTO items (category_id, article, quantity, expiry_date)
VALUES
    (1, 'penne', 5, 2510),
    (1, 'spaghetti', 8, 2411),
    (2, 'olive', 4, 2406);
