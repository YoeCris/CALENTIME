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
    investigator_last_name VARCHAR(50) NOT NULL,
    investigator_first_name VARCHAR(50) NOT NULL,
    dni VARCHAR(8) NOT NULL,
    reviewer VARCHAR(50),
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    stage ENUM('preparatoria', 'intermedia', 'juzgamiento') NOT NULL,
    deadline TIMESTAMP NOT NULL,
    status ENUM('no revisado', 'en revisión', 'revisado') NOT NULL,
    urgency_level ENUM('verde', 'amarillo', 'rojo', 'azul') NOT NULL,
    review_file VARCHAR(255),
    FOREIGN KEY (reviewer) REFERENCES users(username)
);

-- Tabla case_stages
CREATE TABLE case_stages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_id INT,
    stage ENUM('preparatoria', 'intermedia', 'juzgamiento') NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES cases(id)
);

-- Índices adicionales para optimización
CREATE INDEX idx_cases_reviewer ON cases(reviewer);
CREATE INDEX idx_cases_code ON cases(code);
CREATE INDEX idx_case_stages_case_id ON case_stages(case_id);

DROP DATABASE IF EXISTS gestion_casos;


