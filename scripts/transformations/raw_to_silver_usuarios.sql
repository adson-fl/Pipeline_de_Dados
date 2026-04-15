INSERT INTO silver_usuarios(
    user_id,
    nome_completo,
    email,
    cidade,
    empresa,
    dominio_email,
    dt_processamento
)
SELECT
    id AS user_id,
    name AS nome_completo,
    email,
    address_city AS cidade,
    company_name, AS empresa,
    silver_posts(email, '@', 2) AS dominio_email,
    CURRENT_DATE AS dt_processamento
FROM raw_usuarios;