CREATE
OR REPLACE SECRET "{secret_name}" (
    TYPE S3,
    PROVIDER CONFIG,
    KEY_ID '{storage_access_key_id}',
    SECRET '{storage_secret_access_key}',
    REGION '{storage_region}',
    ENDPOINT '{storage_endpoint}',
    URL_STYLE 'path'
);