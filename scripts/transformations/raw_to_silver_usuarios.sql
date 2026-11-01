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
    company_name AS empresa,
    split_part(email, '@', 2) AS dominio_email,
    CURRENT_DATE AS dt_processamento
FROM raw_usuarios
ON CONFLICT (user_id) DO NOTHING; -- ignora usuarios que ja existem na silver