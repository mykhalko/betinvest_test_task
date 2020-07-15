from enum import Enum
from pathlib import Path

BASE_BATH = Path(__file__).parent.parent
TEMPLATES_PATH = BASE_BATH / "pages"


class StatusCodes(Enum):
    OK = 200


class DB:
    BASE_COLLECTION = "sections"


class APP:
    DB = "db"
