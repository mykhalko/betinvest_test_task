from aiohttp import web
from aiohttp_jinja2 import template as use_html_template

from constants import APP
from core.data_retrievers import load_db_results
from core.results_board import ResultsBoard
from core.schemas import SectionOutputSchema


routes = web.RouteTableDef()


@routes.get("/")
@routes.get("/{search}")
@use_html_template("index.html")
async def view(request):
    board = ResultsBoard.init_from_db(await load_db_results(request.app[APP.DB]))
    search = request.match_info.get("search")
    data = board.filter(search) if search else board.sections
    return {"data": SectionOutputSchema().dump(data, many=True)}
