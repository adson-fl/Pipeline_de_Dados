-- retorna usuarios com email invalido
SELECT * 
FROM silver_usuarios su
WHERE email IS NULL 
    OR email =''
    OR email not like '%@%';