COPY "gold"."condicoes_via"
TO '{storage_path}/condicoes_via.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);