INSERT INTO gold_metricas_usuario (
    user_id,
    nome_usuario,
    cidade,
    empresa,
    total_posts,
    media_palavras_titulo,
    primeiro_post_titulo,
    dt_processamento
)
-- Seletor de posts 
WITH posts_rank AS (
    SELECT
        p.user_id,
        p.titulo,
        p.qtd_palavras_titulo,
        ROW_NUMBER() OVER (PARTITION BY p.user_id ORDER BY p.post_id) as pr
    FROM silver_posts p
),
primeiro_post AS (
    SELECT
        user_id,
        titulo AS primeiro_post_titulo
    FROM posts_rank
    WHERE pr = 1
),
agregados AS (
    SELECT 
        user_id,
        COUNT(*) AS total_posts,
        AVG(qtd_palavras_titulo) AS media_palavras_titulo
    FROM silver_posts
    GROUP BY user_id
)
SELECT 
    u.user_id,
    u.nome_completo AS nome_usuario,
    u.cidade,
    u.empresa,
    a.total_posts,
    a.media_palavras_titulo,
    pp.primeiro_post_titulo,
    CURRENT_DATE AS dt_processamento
FROM silver_usuarios u
LEFT JOIN agregados a ON u.user_id = a.user_id
LEFT JOIN primeiro_post pp ON u.user_id = pp.user_id
ON CONFLICT (user_id) DO NOTHING; -- ignora usuarios que ja existem na gold