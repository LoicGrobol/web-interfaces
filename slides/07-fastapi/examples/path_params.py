from fastapi import FastAPI, HTTPException

app = FastAPI()


SURNAMES = {
    "lancelot": "the brave",
    "bedevere": "the wise",
    "galahad": "the chaste",
    "robin": "the not-quite-so-brave-as-sir-lancelot",
    "tim": "the enchanter (not a knight)"
}


@app.get("/knights/{knight_name}")
async def surname(knight_name):
    try:
        return {"surname": SURNAMES[knight_name]}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Item {knight_name} not found") from e
