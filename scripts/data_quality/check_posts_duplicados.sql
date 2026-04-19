-- posts duplicados 
SELECT post_id, COUNT(*) AS qtd
FROM silver_posts
GROUP BY post_id
HAVING COUNT(*) > 1;