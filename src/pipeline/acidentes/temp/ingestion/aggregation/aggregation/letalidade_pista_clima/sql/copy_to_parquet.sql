COPY "gold"."agg_letalidade_pista_clima"
TO '{storage_path}/agg_letalidade_pista_clima.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);