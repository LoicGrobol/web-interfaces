from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import spacy

app = FastAPI()


class InputData(BaseModel):
    sentence: str


@app.post("/postag")
async def postag(inpt: InputData, model="fr_core_news_sm"):
    if model not in spacy.util.get_installed_models():
        raise HTTPException(status_code=422, detail=f"Model {model!r} unavailable")
    nlp = spacy.load(model)
    doc = nlp(inpt.sentence)
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
    lst = "\n".join([f"<li>{w.text}: {w.pos_}</li>" for w in doc])
    html_content = "\n".join([above, lst, below])
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/list")
async def list_models():
    return {"models": spacy.util.get_installed_models()}