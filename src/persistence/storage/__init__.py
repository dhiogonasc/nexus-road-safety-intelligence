from os import getenv

from .settings import BucketSettings

env_profile = getenv("ENV", "dev")
ENV_FILE = f".env.{env_profile}"

bucket_settings = BucketSettings(_env_file=ENV_FILE)
