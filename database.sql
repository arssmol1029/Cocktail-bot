CREATE DATABASE cocktail_bot;

CREATE TABLE IF NOT EXISTS cocktails (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    url VARCHAR(255) DEFAULT NULL,
    description TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ingredients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cocktail_ingredients (
    PRIMARY KEY (cocktail_id, ingredient_id),
    FOREIGN KEY (cocktail_id) REFERENCES cocktails(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE,
    amount VARCHAR(100)
);