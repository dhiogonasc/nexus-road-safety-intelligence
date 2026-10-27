COPY "gold"."agg_sazonalidade"
TO '{storage_path}/agg_sazonalidade.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);