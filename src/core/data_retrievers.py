from typing import Dict, List

import pymongo
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError
from motor.motor_asyncio import AsyncIOMotorClient

from conf import Configuration
from constants import StatusCodes, DB


async def load_web_results(url: str = Configuration.BASE_DATA_URL, headers: Dict = None) -> Dict:
    """
    Fetch raw data from web uri

    :param url: web uri for data retrieval
    :param headers: additional headers
    :return: json body of response
    """
    async with ClientSession() as session:
        async with session.get(url, headers=headers or {}) as response:
            if response.status != StatusCodes.OK.value:
                raise ClientError(f"Bad status code for url <{url}>")
            return await response.json()


async def load_db_results(db: AsyncIOMotorClient) -> List[Dict]:
    """
    Fetch all data from database sorted by id without mongoDB _id field

    :param db: application db instance
    :return: list of documents
    """
    return await db[DB.BASE_COLLECTION].find({}, {"_id": False}).sort("id", pymongo.ASCENDING).to_list(None)
