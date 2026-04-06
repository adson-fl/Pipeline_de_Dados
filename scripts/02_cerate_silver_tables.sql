CREATE TABLE silver_usuarios (
    user_id INTEGER PRIMARY KEY,
    nome_completo VARCHAR (255),
    email VARCHAR (255),
    cidade VARCHAR (255),
    empresa VARCHAR (255),
    dominio_email VARCHAR(255),
    dt_processamento DATA
);

CREATE TABLE silver_posts (
    post_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    titulo TEXT,
    conteudo TEXT,
    qtd_palavras_titulo INTEGER,
    dt_processamento DATA
);