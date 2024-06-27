-- Crear base de datos
CREATE DATABASE gestion_casos;
USE gestion_casos;

-- Tabla users
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('administrador', 'usuario') NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    dni VARCHAR(8) UNIQUE NOT NULL
);

-- Tabla cases
CREATE TABLE cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    investigated_last_name VARCHAR(50) NOT NULL,
    investigated_first_name VARCHAR(50) NOT NULL,
    dni VARCHAR(8) NOT NULL,
    reviewer VARCHAR(50),
    stage ENUM('preparatoria', 'intermedia', 'juzgamiento') NOT NULL,
    review_file VARCHAR(255),
    FOREIGN KEY (reviewer) REFERENCES users(username)
);

ALTER TABLE cases
DROP COLUMN review_file;

DESCRIBE cases;
