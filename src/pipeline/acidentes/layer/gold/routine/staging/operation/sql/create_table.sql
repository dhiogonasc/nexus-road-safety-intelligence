CREATE OR REPLACE "gold"."stg_ft_ocorrencia" AS
SELECT * FROM read_parquet('{silver_storage_path}/ft_ocorrencia/**/*.parquet');