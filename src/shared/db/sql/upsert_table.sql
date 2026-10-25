SELECT setval(
    'seq_{table.name}', 
    GREATEST(COALESCE((SELECT MAX(id) FROM {table.fqn}), 0), 1)
);

CREATE TEMP TABLE "temp_{table.name}" AS 
SELECT 
    nextval('seq_{table.name}') AS id,
    {table.columns_names}
FROM (
    SELECT {table.unique_columns_names}
    FROM "silver"."last_charge"
);

MERGE INTO {table.fqn} AS target 
USING 'temp_{table.name}' AS source 
    ON {merge_reference}

WHEN NOT MATCHED THEN 
INSERT ({table.columns_names}) 
VALUES ({source_columns_names});

DROP TABLE IF EXISTS "temp_{table.name}";