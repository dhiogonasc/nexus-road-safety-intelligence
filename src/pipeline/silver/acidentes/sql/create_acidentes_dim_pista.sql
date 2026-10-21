CREATE TABLE IF NOT EXISTS "silver"."dim_pista" (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_carga VARCHAR,
    condicao_metereologica VARCHAR,
    sentido_via VARCHAR,
    tracado_via VARCHAR,
    tipo_pista VARCHAR,
    uso_solo VARCHAR
);

BEGIN TRANSACTION;
TRY
INSERT INTO "silver"."dim_pista" (
    id_carga, condicao_metereologica, 
    sentido_via, tracado_via, tipo_pista, 
    uso_solo
)
SELECT 
    id_carga, condicao_metereologica, 
    sentido_via, tracado_via, tipo_pista, 
    uso_solo
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/silver/dim_pista/*.parquet')
WHERE (
    id_carga, condicao_metereologica, 
    sentido_via, tracado_via, tipo_pista, 
    uso_solo
) NOT IN (
    SELECT
        id_carga, condicao_metereologica, 
        sentido_via, tracado_via, tipo_pista, 
        uso_solo 
    FROM "silver"."dim_pista"
);
CATCH
END TRY;
COMMIT;

CREATE TEMP TABLE temp_ocorrencias AS 
SELECT DISTINCT 
    id_carga,
    COALESCE(condicao_metereologica :: VARCHAR, 'nao_informado') AS condicao_metereologica,
    COALESCE(sentido_via :: VARCHAR, 'nao_informado') AS sentido_via,
    COALESCE(tracado_via :: VARCHAR, 'nao_informado') AS tracado_via,
    COALESCE(tipo_pista :: VARCHAR, 'nao_informado') AS tipo_pista,
    COALESCE(uso_solo :: VARCHAR, 'nao_informado') AS uso_solo
FROM read_parquet('s3://{settings.STORAGE_BUCKET}/acidentes/bronze/ocorrencias/**/*.parquet');


MERGE INTO "silver"."dim_pista" AS target 
USING temp_ocorrencias AS source 
ON target.condicao_metereologica = source.condicao_metereologica
AND target.sentido_via = source.sentido_via
AND target.tracado_via = source.tracado_via
AND target.tipo_pista = source.tipo_pista
AND target.uso_solo = source.uso_solo


WHEN MATCHED AND target.id_carga <> source.id_carga THEN 
    UPDATE SET 
        id_carga = source.id_carga,
        condicao_metereologica = source.condicao_metereologica,
        sentido_via = source.sentido_via,
        tracado_via = source.tracado_via,
        tipo_pista = source.tipo_pista,
        uso_solo = source.uso_solo

WHEN NOT MATCHED THEN 
    INSERT (id_carga, condicao_metereologica, sentido_via, tracado_via, tipo_pista, uso_solo) 
    VALUES (
        source.id_carga, 
        source.condicao_metereologica, 
        source.sentido_via, 
        source.tracado_via, 
        source.tipo_pista, 
        source.uso_solo
    );

COPY "silver"."dim_pista" 
TO 's3://{settings.STORAGE_BUCKET}/{domain}/silver/dim_pista/' 
(FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);

DROP TABLE IF EXISTS temp_ocorrencias;