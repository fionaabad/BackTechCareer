import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Config BBDD
    DB_HOST: str | None = os.getenv("DB_HOST")
    DB_USER: str | None = os.getenv("DB_USER")
    DB_PASSWORD: str | None = os.getenv("DB_PASSWORD")
    DB_NAME: str | None = os.getenv("DB_NAME")

    # Config Gemini / LLM
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")


settings = Settings()
