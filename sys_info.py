import psutil
from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/api/cpu")
async def cpu(request):
    return web.json_response({"use": psutil.cpu_percent(interval=1)})


@routes.get("/api/memory")
async def memory(request):
    mem = psutil.virtual_memory()
    return web.json_response({"total": round(mem.total/1024/1024, 2),
                              "free": round(mem.available/1024/1024, 2),
                              "used": round(mem.active/1024/1024, 2)})


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=8080)
