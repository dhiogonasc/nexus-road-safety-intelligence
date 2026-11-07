from pydantic_settings import BaseSettings


class StorageSettings(BaseSettings):
    STORAGE_BUCKET: str = "bucket"
    STORAGE_ENDPOINT: str = "http://localhost:3900"
    STORAGE_REGION: str = "region"
    STORAGE_ACCESS_KEY_ID: str = ""
    STORAGE_SECRET_ACCESS_KEY: str = ""

    @property
    def conn_config(self) -> str:
        return (
            f"ENDPOINT '{self.STORAGE_ENDPOINT}', \n"
            f"KEY_ID '{self.STORAGE_ACCESS_KEY_ID}', \n"
            f"SECRET '{self.STORAGE_SECRET_ACCESS_KEY}', \n"
            f"REGION '{self.STORAGE_REGION}', \n"
        )

    @property
    def base_uri(self) -> str:
        return f"s3://{self.STORAGE_BUCKET}"
