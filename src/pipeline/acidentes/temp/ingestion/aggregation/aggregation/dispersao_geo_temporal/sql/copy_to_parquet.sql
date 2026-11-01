COPY "gold"."agg_dispersao_geo_temporal"
TO '{storage_path}/agg_dispersao_geo_temporal.parquet' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);