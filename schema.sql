CREATE TABLE IF NOT EXISTS users (
    tg_id INTEGER PRIMARY KEY,
    name TEXT,
    surname TEXT,
    reffer_code TEXT unique
);

CREATE TABLE IF NOT EXISTS free_orders (
    id INTEGER PRIMARY KEY,
    timestamp INTEGER unique
);