COPY "gold"."agg_letalidade_clima_tempo"
TO '{storage_path}/agg_letalidade_clima_tempo.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);