CREATE OR REPLACE TABLE "gold"."stage" AS 
SELECT * FROM read_parquet('{silver_ft_storage_path}/**/*.parquet')