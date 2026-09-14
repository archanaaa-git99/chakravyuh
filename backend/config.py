# backend/config.py

import os


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./chakravyuh.db")
    APP_NAME: str = "CHAKRAVYUH - Database & Correlation Module"


settings = Settings()
