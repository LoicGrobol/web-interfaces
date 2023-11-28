from fastapi import FastAPI, HTTPException

app = FastAPI()


SURNAMES = {
    "lancelot": "the brave",
    "bedevere": "the wise",
    "galahad": "the chaste",
    "robin": "the not-quite-so-brave-as-sir-lancelot",
    "tim": "the enchanter (not a knight)"
}


@app.get("/knights/")
async def surname(name):
    try:
        return {"surname": SURNAMES[name]}
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Item {name} not found")
