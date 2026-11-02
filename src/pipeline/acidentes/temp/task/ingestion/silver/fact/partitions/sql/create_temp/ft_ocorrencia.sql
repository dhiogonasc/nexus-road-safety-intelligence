CREATE TABLE IF NOT EXISTS "silver"."temp_ft_ocorrencia" AS
SELECT * EXCLUDE (id) FROM "silver"."ft_ocorrencia";