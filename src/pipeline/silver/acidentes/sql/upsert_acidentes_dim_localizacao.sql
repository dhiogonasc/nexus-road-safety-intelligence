CREATE TEMP TABLE temp_ocorrencias_localizacao AS 
SELECT 
    COALESCE((SELECT MAX(id) FROM "silver"."dim_localizacao"), 0) + ROW_NUMBER() OVER () AS id,
    source_data.id_carga,
    source_data.uf,
    source_data.br,
    source_data.municipio,
    source_data.regional,
    source_data.delegacia,
    source_data.uop,
    source_data.km
FROM (
    SELECT 
        MAX(id_carga) AS id_carga, 
        TRIM(COALESCE(uf :: VARCHAR, 'nao_informado')) AS uf,
        TRIM(COALESCE(br :: VARCHAR, 'nao_informado')) AS br,
        TRIM(COALESCE(municipio :: VARCHAR, 'nao_informado')) AS municipio,
        TRIM(COALESCE(regional :: VARCHAR, 'nao_informado')) AS regional,
        TRIM(COALESCE(delegacia :: VARCHAR, 'nao_informado')) AS delegacia,
        TRIM(COALESCE(uop :: VARCHAR, 'nao_informado')) AS uop,
        TRY_CAST(REPLACE(km :: VARCHAR, ',', '.') AS DOUBLE) AS km
    FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet')
    GROUP BY 2, 3, 4, 5, 6, 7, 8
) AS source_data;

MERGE INTO "silver"."dim_localizacao" AS target 
USING temp_ocorrencias_localizacao AS source 
    ON target.uf = source.uf
    AND target.br = source.br
    AND target.municipio = source.municipio
    AND target.regional = source.regional
    AND target.delegacia = source.delegacia
    AND target.uop = source.uop
    AND target.km = source.km

WHEN MATCHED AND target.id_carga <> source.id_carga THEN 
    UPDATE SET 
        id_carga = source.id_carga,
        uf = source.uf,
        br = source.br,
        municipio = source.municipio,
        regional = source.regional,
        delegacia = source.delegacia,
        uop = source.uop,
        km = source.km

WHEN NOT MATCHED THEN 
    INSERT (
        id, id_carga, uf, br, 
        municipio, regional, delegacia, 
        uop, km
    ) 
    VALUES (
        source.id,
        source.id_carga, 
        source.uf, 
        source.br, 
        source.municipio, 
        source.regional, 
        source.delegacia, 
        source.uop,
        source.km
    );

DROP TABLE IF EXISTS temp_ocorrencias_localizacao;