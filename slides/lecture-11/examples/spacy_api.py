from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
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
    return {"tags": [w.pos_ for w in doc]}


@app.get("/list")
async def list_models():
    return {"models": spacy.util.get_installed_models()}