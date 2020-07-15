from aiohttp import web

from .utils import init_app, populate_db
from .views import routes


def create_app() -> web.Application:
    app = web.Application()
    app.add_routes(routes)
    init_app(app)
    app.on_startup.append(populate_db)
    return app
