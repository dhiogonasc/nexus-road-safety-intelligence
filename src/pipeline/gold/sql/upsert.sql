INSERT INTO {full_target} ({cols_str})
SELECT {cols_str}
FROM {full_source}
ON CONFLICT ({conflict_str}) DO UPDATE SET {update_str};