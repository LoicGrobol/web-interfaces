from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# Le paramètre `request` est obligatoire, c'est la faute à Starlette !
@app.get("/hello/{name}", response_class=HTMLResponse)
async def read_item(request: Request, name: str):
    return templates.TemplateResponse(
        "hello.html.jinja", {"request": request, "name": name}
    )
