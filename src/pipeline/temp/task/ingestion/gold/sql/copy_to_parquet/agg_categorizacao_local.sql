COPY "gold"."agg_categorizacao_local"
TO '{storage_path}/agg_categorizacao_local.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);