-- Crear base de datos
CREATE DATABASE gestion_casos;
USE gestion_casos;

-- Tabla users
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(10) UNIQUE NOT NULL,
    password VARCHAR(6) NOT NULL,
    role ENUM('administrador', 'usuario') NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    dni VARCHAR(8) UNIQUE NOT NULL
);

-- Tabla cases
CREATE TABLE cases (
    case_id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    investigated_last_name VARCHAR(20) NOT NULL,
    investigated_first_name VARCHAR(20) NOT NULL,
    dni VARCHAR(8) NOT NULL,
    reviewer VARCHAR(10),
    stage ENUM('preparatoria', 'intermedia', 'juzgamiento') NOT NULL,
    FOREIGN KEY (reviewer) REFERENCES users(username)
);

INSERT INTO users (username, password, role, first_name, last_name, dni) VALUES
('jdoe', 'abc123', 'usuario', 'John', 'Doe', '12345678'),
('asmith', 'def456', 'usuario', 'Alice', 'Smith', '23456789'),
('bwhite', 'ghi789', 'usuario', 'Bob', 'White', '34567890'),
('cgreen', 'jkl012', 'usuario', 'Charlie', 'Green', '45678901'),
('dblack', 'mno345', 'usuario', 'David', 'Black', '56789012');

INSERT INTO cases (code, investigated_last_name, investigated_first_name, dni, reviewer, stage) VALUES
('C001', 'Smith', 'John', '12345678', 'jdoe', 'preparatoria'),
('C002', 'Doe', 'Jane', '23456789', 'asmith', 'intermedia'),
('C003', 'Black', 'Alice', '34567890', 'bwhite', 'juzgamiento'),
('C004', 'White', 'Charlie', '45678901', 'cgreen', 'preparatoria'),
('C005', 'Green', 'David', '56789012', 'dblack', 'intermedia'),
('C006', 'Doe', 'Alice', '12345678', 'jdoe', 'juzgamiento'),
('C007', 'Smith', 'Charlie', '23456789', 'asmith', 'preparatoria'),
('C008', 'Black', 'John', '34567890', 'bwhite', 'intermedia'),
('C009', 'White', 'Jane', '45678901', 'cgreen', 'juzgamiento'),
('C010', 'Green', 'Bob', '56789012', 'dblack', 'preparatoria'),
('C011', 'Doe', 'Charlie', '12345678', 'jdoe', 'intermedia'),
('C012', 'Smith', 'David', '23456789', 'asmith', 'juzgamiento'),
('C013', 'Black', 'John', '34567890', 'bwhite', 'preparatoria'),
('C014', 'White', 'Alice', '45678901', 'cgreen', 'intermedia'),
('C015', 'Green', 'Jane', '56789012', 'dblack', 'juzgamiento'),
('C016', 'Doe', 'David', '12345678', 'jdoe', 'preparatoria'),
('C017', 'Smith', 'John', '23456789', 'asmith', 'intermedia'),
('C018', 'Black', 'Jane', '34567890', 'bwhite', 'juzgamiento'),
('C019', 'White', 'Bob', '45678901', 'cgreen', 'preparatoria'),
('C020', 'Green', 'Alice', '56789012', 'dblack', 'intermedia'),
('C021', 'Doe', 'Bob', '12345678', 'jdoe', 'juzgamiento'),
('C022', 'Smith', 'Alice', '23456789', 'asmith', 'preparatoria'),
('C023', 'Black', 'Charlie', '34567890', 'bwhite', 'intermedia'),
('C024', 'White', 'David', '45678901', 'cgreen', 'juzgamiento'),
('C025', 'Green', 'John', '56789012', 'dblack', 'preparatoria'),
('C026', 'Doe', 'Alice', '12345678', 'jdoe', 'intermedia'),
('C027', 'Smith', 'Jane', '23456789', 'asmith', 'juzgamiento'),
('C028', 'Black', 'Charlie', '34567890', 'bwhite', 'preparatoria'),
('C029', 'White', 'David', '45678901', 'cgreen', 'intermedia'),
('C030', 'Green', 'John', '56789012', 'dblack', 'juzgamiento'),
('C031', 'Doe', 'Charlie', '12345678', 'jdoe', 'preparatoria'),
('C032', 'Smith', 'David', '23456789', 'asmith', 'intermedia'),
('C033', 'Black', 'Alice', '34567890', 'bwhite', 'juzgamiento'),
('C034', 'White', 'Jane', '45678901', 'cgreen', 'preparatoria'),
('C035', 'Green', 'Bob', '56789012', 'dblack', 'intermedia'),
('C036', 'Doe', 'David', '12345678', 'jdoe', 'juzgamiento'),
('C037', 'Smith', 'John', '23456789', 'asmith', 'preparatoria'),
('C038', 'Black', 'Jane', '34567890', 'bwhite', 'intermedia'),
('C039', 'White', 'Alice', '45678901', 'cgreen', 'juzgamiento'),
('C040', 'Green', 'Charlie', '56789012', 'dblack', 'preparatoria'),
('C041', 'Doe', 'Jane', '12345678', 'jdoe', 'intermedia'),
('C042', 'Smith', 'Charlie', '23456789', 'asmith', 'juzgamiento'),
('C043', 'Black', 'Bob', '34567890', 'bwhite', 'preparatoria'),
('C044', 'White', 'David', '45678901', 'cgreen', 'intermedia'),
('C045', 'Green', 'John', '56789012', 'dblack', 'juzgamiento'),
('C046', 'Doe', 'Alice', '12345678', 'jdoe', 'preparatoria'),
('C047', 'Smith', 'Bob', '23456789', 'asmith', 'intermedia'),
('C048', 'Black', 'Charlie', '34567890', 'bwhite', 'juzgamiento'),
('C049', 'White', 'Jane', '45678901', 'cgreen', 'preparatoria'),
('C050', 'Green', 'David', '56789012', 'dblack', 'intermedia');
