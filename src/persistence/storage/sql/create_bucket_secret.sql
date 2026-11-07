CREATE
OR REPLACE SECRET "{settings.STORAGE_BUCKET}" (
    TYPE S3,
    PROVIDER CONFIG,
    {settings.conn_config}
    URL_STYLE 'path'
);