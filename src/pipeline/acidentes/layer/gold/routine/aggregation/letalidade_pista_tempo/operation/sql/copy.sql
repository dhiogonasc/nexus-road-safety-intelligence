COPY "gold"."agg_letalidade_pista_tempo"
TO '{storage_path}/agg_letalidade_pista_tempo.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);