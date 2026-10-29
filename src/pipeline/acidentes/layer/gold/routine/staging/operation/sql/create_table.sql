CREATE OR REPLACE TABLE "gold"."stg" AS 
SELECT * FROM read_parquet('{storage_path}/**/*.parquet')