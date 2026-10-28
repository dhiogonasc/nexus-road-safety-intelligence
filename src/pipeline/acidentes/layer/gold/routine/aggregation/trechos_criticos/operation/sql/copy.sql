COPY "gold"."agg_trechos_criticos"
TO '{storage_path}/agg_trechos_criticos.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);