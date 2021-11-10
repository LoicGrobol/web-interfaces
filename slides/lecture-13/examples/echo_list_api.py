from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()


class InputData(BaseModel):
    lines: List[str]


@app.post("/", response_class=HTMLResponse)
async def display(inpt: InputData):
    above = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>This is what you asked me to display</title>
  </head>
  <body>
  <ol>
"""
    below = """
  </ol>
  </body>
</html>
"""
    lst = "\n".join([f"<li>{name}</li>" for name in inpt.lines])
    html_content = "\n".join([above, lst, below])
    return HTMLResponse(content=html_content, status_code=200)