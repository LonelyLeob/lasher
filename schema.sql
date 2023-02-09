CREATE TABLE IF NOT EXISTS users (
    tg_id INTEGER PRIMARY KEY,
    name TEXT,
    surname TEXT,
    reffer_code TEXT unique,
    reffer_quantity INTEGER
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER unique,
    busyby INTEGER
);

CREATE TABLE IF NOT EXISTS pricelist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price FLOAT
);