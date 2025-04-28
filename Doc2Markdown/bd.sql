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
    original_format VARCHAR(20) NOT NULL, 
    markdown_content TEXT,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
	version INT NULL
);

/*Pass: 123*/
INSERT INTO users (username, email, password_hash) 
VALUES ('Jaime', 'jaime.doe@example.com', '$2b$12$40EHCl91BqgJsvJ8XAXwzuoZ4sGze4pCroHcjqM6W419UNJtDrXtK'),
       ('Yoelito', 'yoelito.smith@example.com', '$2b$12$40EHCl91BqgJsvJ8XAXwzuoZ4sGze4pCroHcjqM6W419UNJtDrXtK'),
	   ('Elvicito', 'elvicito.smith@example.com', '$2b$12$40EHCl91BqgJsvJ8XAXwzuoZ4sGze4pCroHcjqM6W419UNJtDrXtK');

INSERT INTO documents (user_id, title, original_format, markdown_content) 
VALUES (1, 'Sample Document 1', 'DOC', 'This is the content of the document in markdown format.'), 
       (2, 'Sample Document 2', 'DOCX', 'Another markdown content here.'),
	   (3, 'Sample Document 3', 'DOCX', 'Another markdown content here.');

