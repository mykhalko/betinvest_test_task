import os

APP_PORT = int(os.getenv("APP_PORT", 8989))
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "27017")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "betinvest")

BASE_DATA_URL = os.getenv(
    "BASE_DATA_URL",
    "https://clientsapi12.bkfon-resource.ru/results/results.json.php?locale=ru"
)


class Configuration:
    """
    Container for storing app configuration

    """
    def __init__(self):
        auth = ""
        if self.DB_USER and self.DB_PASSWORD:
            auth = f"{self.DB_USER}:{self.DB_PASSWORD}@"
        self.DB_URI = f"mongo://{auth}{self.DB_HOST}:{self.DB_PORT}"

    APP_PORT = APP_PORT
    APP_HOST = APP_HOST

    DB_HOST = DB_HOST
    DB_PORT = DB_PORT
    DB_USER = DB_USER
    DB_PASSWORD = DB_PASSWORD
    DB_NAME = DB_NAME
    DB_URI = None

    BASE_DATA_URL = BASE_DATA_URL
