import aiohttp
import jinja2
import aiohttp_jinja2
from aiohttp import web
from secrets import yandex
from data import Point, default_point_factory
from utils import split_list

routes = web.RouteTableDef()


@routes.get("/")
@aiohttp_jinja2.template("index.html")
async def index(request):

    points = Point.select()

    init_point = points[0] if points else default_point_factory()

    lines = [line for line in split_list(points, lambda p: p.is_newline)]

    return {"points": points,
            "token": yandex,
            "init_point": init_point,
            "lines": lines}


class WebServer:
    def __init__(self):
        self._app = web.Application()
        self._app.router.add_routes(routes)
        self._runner = web.AppRunner(self._app)

        aiohttp_jinja2.setup(self._app, loader=jinja2.FileSystemLoader("."))

    async def run(self):
        await self._runner.setup()

        site = web.TCPSite(self._runner, port=8081)
        await site.start()
