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
    deadline DATE DEFAULT CURRENT_DATE,
    stage ENUM('preparatoria', 'intermedia', 'juzgamiento') NOT NULL,
    FOREIGN KEY (reviewer) REFERENCES users(username)
);

INSERT INTO users (username, password, role, first_name, last_name, number_phone, dni) VALUES
('emanol', 'emanol', 'usuario', 'Emanol Jesus', 'Tito Melo', '987654321', '12345678'),
('mariaj', 'pass13', 'usuario', 'María Jose', 'Sánchez Lopez', '987654322', '87654321'),
('juanh', 'pass14', 'usuario', 'Juan Manuel', 'Flores Huanca', '987654323', '45678901'),
('anam', 'pass15', 'usuario', 'Ana Maria', 'García Miro', '987654324', '65432109'),
('luism', 'pass16', 'usuario', 'Luis Alberto', 'Rojas Perca', '987654325', '78901234');

INSERT INTO cases (code, investigated_last_name, investigated_first_name, dni, reviewer, created_date, deadline, stage) VALUES
('CASE001', 'Ramírez', 'José', '13579246', 'emanol', '2024-01-01', '2024-06-30', 'preparatoria'),
('CASE002', 'Fernández', 'Miguel', '24681357', 'mariaj', '2024-01-15', '2024-07-15', 'preparatoria'),
('CASE003', 'Pérez', 'Ricardo', '35792468', 'juanh', '2024-02-01', '2024-07-30', 'intermedia'),
('CASE004', 'Rodríguez', 'María', '46813579', 'anam', '2024-02-15', '2024-08-15', 'intermedia'),
('CASE005', 'López', 'Carmen', '57924681', 'luism', '2024-03-01', '2024-08-30', 'juzgamiento'),
('CASE006', 'González', 'Luis', '68135792', 'anam', '2024-03-15', '2024-09-15', 'juzgamiento'),
('CASE007', 'Martínez', 'Ana', '79246813', 'luism', '2024-04-01', '2024-09-30', 'preparatoria'),
('CASE008', 'Torres', 'José', '81357924', 'emanol', '2024-04-15', '2024-10-15', 'preparatoria'),
('CASE009', 'Ramírez', 'Juan', '92468135', 'mariaj', '2024-05-01', '2024-10-30', 'intermedia'),
('CASE010', 'Fernández', 'Miguel', '13579246', 'mariaj', '2024-05-15', '2024-11-15', 'intermedia'),
('CASE011', 'Pérez', 'Carlos', '24681357', 'juanh', '2024-06-01', '2024-11-30', 'juzgamiento'),
('CASE012', 'Rodríguez', 'Ana', '35792468', 'juanh', '2024-06-15', '2024-12-15', 'juzgamiento'),
('CASE013', 'López', 'Ricardo', '46813579', 'anam', '2024-07-01', '2024-12-30', 'preparatoria'),
('CASE014', 'González', 'Luis', '57924681', 'anam', '2024-07-15', '2025-01-15', 'preparatoria'),
('CASE015', 'Martínez', 'Carmen', '68135792', 'luism', '2024-08-01', '2025-01-30', 'intermedia'),
('CASE016', 'Torres', 'Juan', '79246813', 'luism', '2024-08-15', '2025-02-15', 'intermedia'),
('CASE017', 'Ramírez', 'José', '81357924', 'emanol', '2024-09-01', '2025-02-28', 'juzgamiento'),
('CASE018', 'Fernández', 'Miguel', '92468135', 'emanol', '2024-09-15', '2025-03-15', 'juzgamiento'),
('CASE019', 'Pérez', 'Ricardo', '13579246', 'mariaj', '2024-10-01', '2025-03-30', 'preparatoria'),
('CASE020', 'Rodríguez', 'María', '24681357', 'mariaj', '2024-10-15', '2025-04-15', 'preparatoria'),
('CASE021', 'López', 'Carmen', '35792468', 'juanh', '2024-11-01', '2025-04-30', 'intermedia'),
('CASE022', 'González', 'Luis', '46813579', 'juanh', '2024-11-15', '2025-05-15', 'intermedia'),
('CASE023', 'Martínez', 'Ana', '57924681', 'anam', '2024-12-01', '2025-05-30', 'juzgamiento'),
('CASE024', 'Torres', 'José', '68135792', 'anam', '2024-12-15', '2025-06-15', 'juzgamiento'),
('CASE025', 'Ramírez', 'Juan', '79246813', 'luism', '2024-01-02', '2024-07-01', 'preparatoria'),
('CASE026', 'Fernández', 'Miguel', '81357924', 'luism', '2024-01-16', '2024-07-16', 'preparatoria'),
('CASE027', 'Pérez', 'Carlos', '92468135', 'emanol', '2024-02-02', '2024-08-01', 'intermedia'),
('CASE028', 'Rodríguez', 'Ana', '13579246', 'emanol', '2024-02-16', '2024-08-16', 'intermedia'),
('CASE029', 'López', 'Ricardo', '24681357', 'mariaj', '2024-03-02', '2024-08-31', 'juzgamiento'),
('CASE030', 'González', 'Luis', '35792468', 'mariaj', '2024-03-16', '2024-09-16', 'juzgamiento'),
('CASE031', 'Martínez', 'Carmen', '46813579', 'juanh', '2024-04-02', '2024-09-30', 'preparatoria'),
('CASE032', 'Torres', 'Juan', '57924681', 'juanh', '2024-04-16', '2024-10-16', 'preparatoria'),
('CASE033', 'Ramírez', 'José', '68135792', 'anam', '2024-05-02', '2024-10-31', 'intermedia'),
('CASE034', 'Fernández', 'Miguel', '79246813', 'anam', '2024-05-16', '2024-11-16', 'intermedia'),
('CASE035', 'Pérez', 'Ricardo', '81357924', 'luism', '2024-06-02', '2024-11-30', 'juzgamiento'),
('CASE036', 'Rodríguez', 'María', '92468135', 'luism', '2024-06-16', '2024-12-16', 'juzgamiento'),
('CASE037', 'López', 'Carmen', '13579246', 'emanol', '2024-07-02', '2024-12-31', 'preparatoria'),
('CASE038', 'González', 'Luis', '24681357', 'emanol', '2024-07-16', '2025-01-16', 'preparatoria'),
('CASE039', 'Martínez', 'Ana', '35792468', 'mariaj', '2024-08-02', '2025-01-31', 'intermedia'),
('CASE040', 'Torres', 'José', '46813579', 'mariaj', '2024-08-16', '2025-02-16', 'intermedia'),
('CASE041', 'Ramírez', 'Juan', '57924681', 'juanh', '2024-09-02', '2025-02-28', 'juzgamiento'),
('CASE042', 'Fernández', 'Miguel', '68135792', 'juanh', '2024-09-16', '2025-03-16', 'juzgamiento'),
('CASE043', 'Pérez', 'Carlos', '79246813', 'anam', '2024-10-02', '2025-03-31', 'preparatoria'),
('CASE044', 'Rodríguez', 'Ana', '81357924', 'anam', '2024-10-16', '2025-04-16', 'preparatoria'),
('CASE045', 'López', 'Ricardo', '92468135', 'luism', '2024-11-02', '2025-04-30', 'intermedia'),
('CASE046', 'González', 'Luis', '13579246', 'luism', '2024-11-16', '2025-05-16', 'intermedia'),
('CASE047', 'Martínez', 'Carmen', '24681357', 'emanol', '2024-12-02', '2025-05-31', 'juzgamiento'),
('CASE048', 'Torres', 'Juan', '35792468', 'emanol', '2024-12-16', '2025-06-16', 'juzgamiento'),
('CASE049', 'Ramírez', 'José', '46813579', 'mariaj', '2024-01-03', '2024-07-02', 'preparatoria'),
('CASE050', 'Fernández', 'Miguel', '57924681', 'mariaj', '2024-01-17', '2024-07-17', 'preparatoria');