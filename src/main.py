from aiohttp.web import run_app

from conf import Configuration
from web_app.app import create_app


if __name__ == "__main__":
    app = create_app()
    run_app(app, port=Configuration.APP_PORT, host=Configuration.APP_HOST)
