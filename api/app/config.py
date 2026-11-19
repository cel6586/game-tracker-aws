""" Holds settings, secrets, keys, urls """

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    """  Settings for database and security """
    database_url: str | None = None
    db_host: str | None = None
    db_port: int = 5432
    db_name: str = "gametracker"
    db_user: str = "gtadmin"
    db_password: str | None = None
    secret_key: str
    signup_code: str | None = None
    # only needed for the game search, without them search returns a 502
    igdb_client_id: str | None = None
    igdb_client_secret: str | None = None
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 40
    # .env is for running locally, in the cluster these come from the secret
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @model_validator(mode="after")
    def build_database_url(self):
        """ If DATABASE_URL is not set, build it from the separate DB_* settings """
        if self.database_url is None:
            if self.db_host is None or self.db_password is None:
                raise ValueError("set DATABASE_URL, or DB_HOST and DB_PASSWORD")
            self.database_url = URL.create(
                "postgresql+psycopg",
                username=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                database=self.db_name,
            ).render_as_string(hide_password=False)
        return self


settings = Settings()
