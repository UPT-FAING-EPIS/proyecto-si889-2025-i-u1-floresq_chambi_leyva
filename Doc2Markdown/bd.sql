-- Tabla de usuarios
CREATE TABLE users (
    user_id INT PRIMARY KEY IDENTITY(1,1),
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- Tabla de documentos
CREATE TABLE documents (
    document_id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT FOREIGN KEY REFERENCES users(user_id),
    title VARCHAR(255) NOT NULL,
    original_format VARCHAR(20) NOT NULL, -- Ej. DOC, DOCX, PDF
    markdown_content TEXT,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- Tabla de versiones de documentos
CREATE TABLE document_versions (
    version_id INT PRIMARY KEY IDENTITY(1,1),
    document_id INT FOREIGN KEY REFERENCES documents(document_id),
    version_number INT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);

-- Tabla de logs de conversión
CREATE TABLE conversion_logs (
    log_id INT PRIMARY KEY IDENTITY(1,1),
    document_id INT FOREIGN KEY REFERENCES documents(document_id),
    status VARCHAR(50) NOT NULL,
    conversion_type VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);
/*Pass: 123*/
INSERT INTO users (username, email, password_hash) 
VALUES ('Jaime', 'jaime.doe@example.com', '$2b$12$40EHCl91BqgJsvJ8XAXwzuoZ4sGze4pCroHcjqM6W419UNJtDrXtK'),
       ('Yoelito', 'yoelito.smith@example.com', '$2b$12$40EHCl91BqgJsvJ8XAXwzuoZ4sGze4pCroHcjqM6W419UNJtDrXtK');

INSERT INTO documents (user_id, title, original_format, markdown_content) 
VALUES (1, 'Sample Document 1', 'DOC', 'This is the content of the document in markdown format.'), 
       (2, 'Sample Document 2', 'DOCX', 'Another markdown content here.');

INSERT INTO document_versions (document_id, version_number, content) 
VALUES (1, 1, 'Initial version of Sample Document 1 in markdown format.'),
       (2, 1, 'Initial version of Sample Document 2 in markdown format.');

INSERT INTO conversion_logs (document_id, status, conversion_type) 
VALUES (1, 'SUCCESS', 'DOC to MD'),
       (2, 'FAILED', 'DOCX to MD');

