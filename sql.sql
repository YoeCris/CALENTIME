CREATE DATABASE gestion_casos;
USE gestion_casos;

-- Tabla users
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(10) UNIQUE NOT NULL,
    password VARCHAR(20) UNIQUE NOT NULL,
    role ENUM('administrador', 'usuario') NOT NULL,
    first_name VARCHAR(20) UNIQUE NOT NULL,
    last_name VARCHAR(20) UNIQUE NOT NULL,
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
    deadline DATE DEFAULT CURRENT_DATE,
    stage ENUM('preparatoria', 'intermedia', 'juzgamiento') NOT NULL,
    FOREIGN KEY (reviewer) REFERENCES users(first_name)
);

INSERT INTO users (username, password, role, first_name, last_name, number_phone, dni) VALUES
('emanol', 'emanol', 'usuario', 'Emanol Jesus', 'Tito Melo', '987654321', '12345678'),
('mariaj', 'pass13', 'usuario', 'María Jose', 'Sánchez Lopez', '987654322', '87654321'),
('juanh', 'pass14', 'usuario', 'Juan Manuel', 'Flores Huanca', '987654323', '45678901'),
('anam', 'pass15', 'usuario', 'Ana Maria', 'García Miro', '987654324', '65432109'),
('luism', 'pass16', 'usuario', 'Luis Alberto', 'Rojas Perca', '987654325', '78901234');

INSERT INTO cases (code, investigated_last_name, investigated_first_name, dni, reviewer, created_date, deadline, stage) VALUES
('C001', 'Perez', 'Jose', '12345678', 'Emanol Jesus', '2023-01-01', '2023-02-01', 'preparatoria'),
('C002', 'Garcia', 'Ana', '87654321', 'María Jose', '2023-01-02', '2023-02-02', 'intermedia'),
('C003', 'Sanchez', 'Luis', '45678901', 'Juan Manuel', '2023-01-03', '2023-02-03', 'juzgamiento'),
('C004', 'Ramirez', 'Carlos', '65432109', 'Ana Maria', '2023-01-04', '2023-02-04', 'preparatoria'),
('C005', 'Torres', 'Maria', '78901234', 'Luis Alberto', '2023-01-05', '2023-02-05', 'intermedia'),
('C006', 'Flores', 'Jose', '12345678', 'Emanol Jesus', '2023-01-06', '2023-02-06', 'juzgamiento'),
('C007', 'Diaz', 'Ana', '87654321', 'María Jose', '2023-01-07', '2023-02-07', 'preparatoria'),
('C008', 'Martinez', 'Luis', '45678901', 'Juan Manuel', '2023-01-08', '2023-02-08', 'intermedia'),
('C009', 'Gonzalez', 'Carlos', '65432109', 'Ana Maria', '2023-01-09', '2023-02-09', 'juzgamiento'),
('C010', 'Lopez', 'Maria', '78901234', 'Luis Alberto', '2023-01-10', '2023-02-10', 'preparatoria'),
('C011', 'Hernandez', 'Jose', '12345678', 'Emanol Jesus', '2023-01-11', '2023-02-11', 'intermedia'),
('C012', 'Fernandez', 'Ana', '87654321', 'María Jose', '2023-01-12', '2023-02-12', 'juzgamiento'),
('C013', 'Rodriguez', 'Luis', '45678901', 'Juan Manuel', '2023-01-13', '2023-02-13', 'preparatoria'),
('C014', 'Perez', 'Carlos', '65432109', 'Ana Maria', '2023-01-14', '2023-02-14', 'intermedia'),
('C015', 'Garcia', 'Maria', '78901234', 'Luis Alberto', '2023-01-15', '2023-02-15', 'juzgamiento'),
('C016', 'Sanchez', 'Jose', '12345678', 'Emanol Jesus', '2023-01-16', '2023-02-16', 'preparatoria'),
('C017', 'Ramirez', 'Ana', '87654321', 'María Jose', '2023-01-17', '2023-02-17', 'intermedia'),
('C018', 'Torres', 'Luis', '45678901', 'Juan Manuel', '2023-01-18', '2023-02-18', 'juzgamiento'),
('C019', 'Flores', 'Carlos', '65432109', 'Ana Maria', '2023-01-19', '2023-02-19', 'preparatoria'),
('C020', 'Diaz', 'Maria', '78901234', 'Luis Alberto', '2023-01-20', '2023-02-20', 'intermedia'),
('C021', 'Martinez', 'Jose', '12345678', 'Emanol Jesus', '2023-01-21', '2023-02-21', 'juzgamiento'),
('C022', 'Gonzalez', 'Ana', '87654321', 'María Jose', '2023-01-22', '2023-02-22', 'preparatoria'),
('C023', 'Lopez', 'Luis', '45678901', 'Juan Manuel', '2023-01-23', '2023-02-23', 'intermedia'),
('C024', 'Hernandez', 'Carlos', '65432109', 'Ana Maria', '2023-01-24', '2023-02-24', 'juzgamiento'),
('C025', 'Fernandez', 'Maria', '78901234', 'Luis Alberto', '2023-01-25', '2023-02-25', 'preparatoria'),
('C026', 'Rodriguez', 'Jose', '12345678', 'Emanol Jesus', '2023-01-26', '2023-02-26', 'intermedia'),
('C027', 'Perez', 'Ana', '87654321', 'María Jose', '2023-01-27', '2023-02-27', 'juzgamiento'),
('C028', 'Garcia', 'Luis', '45678901', 'Juan Manuel', '2023-01-28', '2023-02-28', 'preparatoria'),
('C029', 'Sanchez', 'Carlos', '65432109', 'Ana Maria', '2023-01-29', '2023-03-01', 'intermedia'),
('C030', 'Ramirez', 'Maria', '78901234', 'Luis Alberto', '2023-01-30', '2023-03-02', 'juzgamiento'),
('C031', 'Torres', 'Jose', '12345678', 'Emanol Jesus', '2023-01-31', '2023-03-03', 'preparatoria'),
('C032', 'Flores', 'Ana', '87654321', 'María Jose', '2023-02-01', '2023-03-04', 'intermedia'),
('C033', 'Diaz', 'Luis', '45678901', 'Juan Manuel', '2023-02-02', '2023-03-05', 'juzgamiento'),
('C034', 'Martinez', 'Carlos', '65432109', 'Ana Maria', '2023-02-03', '2023-03-06', 'preparatoria'),
('C035', 'Gonzalez', 'Maria', '78901234', 'Luis Alberto', '2023-02-04', '2023-03-07', 'intermedia'),
('C036', 'Lopez', 'Jose', '12345678', 'Emanol Jesus', '2023-02-05', '2023-03-08', 'juzgamiento'),
('C037', 'Hernandez', 'Ana', '87654321', 'María Jose', '2023-02-06', '2023-03-09', 'preparatoria'),
('C038', 'Fernandez', 'Luis', '45678901', 'Juan Manuel', '2023-02-07', '2023-03-10', 'intermedia'),
('C039', 'Rodriguez', 'Carlos', '65432109', 'Ana Maria', '2023-02-08', '2023-03-11', 'juzgamiento'),
('C040', 'Perez', 'Maria', '78901234', 'Luis Alberto', '2023-02-09', '2023-03-12', 'preparatoria'),
('C041', 'Garcia', 'Jose', '12345678', 'Emanol Jesus', '2023-02-10', '2023-03-13', 'intermedia'),
('C042', 'Sanchez', 'Ana', '87654321', 'María Jose', '2023-02-11', '2023-03-14', 'juzgamiento'),
('C043', 'Ramirez', 'Luis', '45678901', 'Juan Manuel', '2023-02-12', '2023-03-15', 'preparatoria'),
('C044', 'Torres', 'Carlos', '65432109', 'Ana Maria', '2023-02-13', '2023-03-16', 'intermedia'),
('C045', 'Flores', 'Maria', '78901234', 'Luis Alberto', '2023-02-14', '2023-03-17', 'juzgamiento'),
('C046', 'Diaz', 'Jose', '12345678', 'Emanol Jesus', '2023-02-15', '2023-03-18', 'preparatoria'),
('C047', 'Martinez', 'Ana', '87654321', 'María Jose', '2023-02-16', '2023-03-19', 'intermedia'),
('C048', 'Gonzalez', 'Luis', '45678901', 'Juan Manuel', '2023-02-17', '2023-03-20', 'juzgamiento'),
('C049', 'Lopez', 'Carlos', '65432109', 'Ana Maria', '2023-02-18', '2023-03-21', 'preparatoria'),
('C050', 'Hernandez', 'Maria', '78901234', 'Luis Alberto', '2023-02-19', '2023-03-22', 'intermedia');