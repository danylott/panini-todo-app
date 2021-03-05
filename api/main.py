from panini import app as panini_app
from aiohttp import web


app = panini_app.App(
    service_name="api",
    host="127.0.0.1",
    port=4222,
    web_server=True,
    web_host="127.0.0.1",
    web_port=8000,
)


@app.http.post("/tasks/create/")
async def create_task(request):
    data = await request.post()
    response = await app.request("create-task", {"title": data["title"]})
    return web.json_response(response)


@app.http.post("/tasks/{id}/toggle/")
async def toggle_task(request):
    response = await app.request("toggle-task", {"id": request.match_info["id"]})
    return web.json_response(response)


@app.http.get("/tasks/")
async def get_tasks(request):
    response = await app.request("get-tasks", {})
    return web.json_response(response)


if __name__ == '__main__':
    app.start()
