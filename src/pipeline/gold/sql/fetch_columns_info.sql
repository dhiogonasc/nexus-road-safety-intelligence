SELECT 
    column_name, 
    data_type 
FROM information_schema.columns 
WHERE table_schema = '{source_schema}' 
    AND table_name = '{source_table}'
ORDER BY ordinal_position;