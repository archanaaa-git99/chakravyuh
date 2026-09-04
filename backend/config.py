import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./chakravyuh.db",
    )
    APP_NAME: str = "CHAKRAVYUH - Database & Correlation Module"
    ETHERSCAN_API_KEY: str = os.getenv("ETHERSCAN_API_KEY", "")


settings = Settings()
