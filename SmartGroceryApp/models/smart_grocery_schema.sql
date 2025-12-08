CREATE DATABASE IF NOT EXISTS SmartGroceryDB;
USE SmartGroceryDB;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS inventory_items;
-- DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS user_saved_recipes;
DROP TABLE IF EXISTS reports;
DROP TABLE IF EXISTS suggested_recipes;
-- DROP TABLE IF EXISTS grocery_categories;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- CREATE TABLE grocery_categories (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(50) NOT NULL UNIQUE
-- );

CREATE TABLE inventory_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    quantity FLOAT NOT NULL,
    expiration_date DATE,
    image_url VARCHAR(255),
    category VARCHAR(50),
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    -- FOREIGN KEY (category_id) REFERENCES grocery_categories(id) ON DELETE SET NULL
);

-- CREATE TABLE recipes (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(100) NOT NULL,
--     ingredients TEXT NOT NULL,
--     instructions TEXT NOT NULL,
--     macros VARCHAR(255)
-- );

CREATE TABLE user_saved_recipes (
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    saved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    recipe_json JSON NOT NULL,
    PRIMARY KEY (user_id, recipe_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    -- FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

CREATE TABLE reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type VARCHAR(50) NOT NULL,
    data_json TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE suggested_recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    recipe_json JSON NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    -- FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);

-- -- Insert default grocery categories
-- INSERT INTO grocery_categories (name) VALUES
--     ('Produce'),
--     ('Dairy'),
--     ('Meat'),
--     ('Seafood'),
--     ('Bakery'),
--     ('Frozen'),
--     ('Pantry'),
--     ('Beverages'),
--     ('Snacks'),
--     ('Condiments'),
--     ('Household'),
--     ('Personal Care'),
--     ('Other');