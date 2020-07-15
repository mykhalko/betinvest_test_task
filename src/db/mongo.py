from motor.motor_asyncio import AsyncIOMotorClient

from conf import Configuration


def get_database() -> AsyncIOMotorClient:
    """
    Create db instance

    :return: AsyncIO mongo motor instance
    """
    return AsyncIOMotorClient(Configuration.DB_URI)[Configuration.DB_NAME]
