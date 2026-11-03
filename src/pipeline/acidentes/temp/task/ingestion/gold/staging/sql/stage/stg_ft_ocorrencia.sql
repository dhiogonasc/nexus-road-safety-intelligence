CREATE OR REPLACE TABLE "gold"."stg_ft_ocorrencia" AS 
SELECT * FROM read_parquet('{source_storage_path}/**/*.parquet');