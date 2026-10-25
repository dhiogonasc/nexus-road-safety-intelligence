CREATE TABLE IF NOT EXISTS {table.fqn} ({table.columns_definition});
CREATE SEQUENCE IF NOT EXISTS "seq_{table.name}" START 1;
CREATE INDEX IF NOT EXISTS "idx_{table.name}" ON {table.fqn} ({table.unique_columns_name});
