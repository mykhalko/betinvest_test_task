from aiohttp.web import Application
import aiohttp_jinja2
import jinja2

from constants import APP, DB, TEMPLATES_PATH
from core.data_retrievers import load_web_results
from core.results_board import ResultsBoard
from db.mongo import get_database


def init_db(app: Application) -> None:
    """
    Init app db
    :param app: Application instance
    :return:
    """
    app[APP.DB] = get_database()


def init_jinja2(app: Application) -> None:
    """
    Init app with jinja2 rendered with tempaltes folders

    :param app: Application instance
    :return:
    """
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(TEMPLATES_PATH)))


def init_app(app: Application) -> None:
    """
    Run initiation
    :param app: Application instance
    :return:
    """
    init_db(app)
    init_jinja2(app)


async def populate_db(app: Application):
    """
    Request data on application start and save to db

    :param app: Application instance
    :return: None
    """
    await app[APP.DB][DB.BASE_COLLECTION].delete_many({})
    result_board = ResultsBoard.init_from_web(await load_web_results())
    await app[APP.DB][DB.BASE_COLLECTION].insert_many(result_board.sections)
