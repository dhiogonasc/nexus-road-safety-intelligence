CREATE TABLE IF NOT EXISTS "silver"."dim_localizacao" (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_carga VARCHAR,
    uf VARCHAR,
    br VARCHAR,
    km DOUBLE,
    municipio VARCHAR,
    regional VARCHAR,
    delegacia VARCHAR,
    uop VARCHAR
);

BEGIN TRANSACTION;
TRY
    INSERT INTO "silver"."dim_localizacao" (
        id_carga, 
        uf, br, km, municipio, 
        regional, delegacia, uop
    )
    SELECT 
        id_carga, 
        uf, br, km, municipio, 
        regional, delegacia, uop
    FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/dim_localizacao/*.parquet')
    WHERE (
        uf, br, km, municipio, 
        regional, delegacia, uop 
    ) NOT IN (
        SELECT 
            uf, br, km, municipio, 
            regional, delegacia, uop 
        FROM "silver"."dim_localizacao"
    );
CATCH
END TRY;
COMMIT;

CREATE TEMP TABLE temp_ocorrencias AS 
SELECT DISTINCT 
    id_carga,
    TRIM(COALESCE(uf :: VARCHAR, 'nao_informado')) AS uf,
    TRIM(COALESCE(br :: VARCHAR, 'nao_informado')) AS br,
    TRIM(COALESCE(municipio :: VARCHAR, 'nao_informado')) AS municipio,
    TRIM(COALESCE(regional :: VARCHAR, 'nao_informado')) AS regional,
    TRIM(COALESCE(delegacia :: VARCHAR, 'nao_informado')) AS delegacia,
    TRIM(COALESCE(uop :: VARCHAR, 'nao_informado')) AS uop
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet')

MERGE INTO "silver"."dim_localizacao" AS target 
USING temp_ocorrencias AS source 
ON target.uf = source.uf
AND target.br = source.br
AND target.municipio = source.municipio
AND target.regional = source.regional
AND target.delegacia = source.delegacia
AND target.uop = source.uop

WHEN MATCHED AND target.id_carga <> source.id_carga THEN 
    UPDATE SET 
        id_carga = source.id_carga,
        uf = source.uf,
        br = source.br,
        municipio = source.municipio,
        regional = source.regional,
        delegacia = source.delegacia,
        uop = source.uop

WHEN NOT MATCHED THEN 
    INSERT (
        id_carga, 
        uf, br, municipio, 
        regional, delegacia, uop
    ) 
    VALUES (
        source.id_carga, 
        source.uf, 
        source.br, 
        source.municipio, 
        source.regional, 
        source.delegacia, 
        source.uop
    );

COPY "silver"."dim_localizacao" 
TO 's3://{settings.STORAGE_BUCKET}/{domain}/silver/dim_localizacao/' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);

DROP TABLE IF EXISTS temp_ocorrencias;