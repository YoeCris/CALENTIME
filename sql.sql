CREATE DATABASE gestion_casos;
USE gestion_casos;

-- Tabla users
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(10) UNIQUE NOT NULL,
    password VARCHAR(20) NOT NULL,
    role ENUM('administrador', 'usuario') NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    number_phone VARCHAR(9) UNIQUE NOT NULL,
    dni VARCHAR(8) UNIQUE NOT NULL
);

-- Tabla cases
CREATE TABLE IF NOT EXISTS cases (
    case_id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    investigated_last_name VARCHAR(20) NOT NULL,
    investigated_first_name VARCHAR(20) NOT NULL,
    dni VARCHAR(8) NOT NULL,
    reviewer VARCHAR(10),
    created_date DATE DEFAULT CURRENT_DATE,
    deadline INTEGER DEFAULT 30,
    stage ENUM('preparatoria', 'intermedia', 'juzgamiento') NOT NULL,
    FOREIGN KEY (reviewer) REFERENCES users(username)
);
