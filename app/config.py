from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4.1-mini"
    OPENAI_EMBED_MODEL: str = "text-embedding-3-small"
    DB_URL: str = "sqlite:///./data/launchpad.db"
    KB_SQLITE_PATH: str = "./data/kb.sqlite"
    DATA_DIR: str = "./data"
    EXPORT_DIR: str = "./exports"
    CATALOG_DOCX_PATH: str = "./VUE Services 2026.docx"
    BIASES_DOCX_PATH: str = "./Biases.docx"
    SKU_XLSX_PATH: str = "./VUE_Services_SKU_Prices.xlsx"
    cors_allow_origins: List[str] = ["*"]
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
