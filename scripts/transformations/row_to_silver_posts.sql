INSERT INTO silver_posts(
    post_id,
    user_id,
    titulo,
    conteudo,
    qtd_palavras_titulo,
    dt_processamento
)
SELECT
    id AS post_id,
    user_id,
    title AS titulo,
    LEFT(REPLACE(COALESCE(body, ''), E'\n', ''), 500) AS conteudo, -- Remove \n e trunca até 500
    COALESCE(array_length(string_to_array(COALESCE(title, ''), ' '), 1), 0) AS qtd_palavras_titulo,
    CURRENT_DATE AS dt_processamento
FROM raw_posts;


