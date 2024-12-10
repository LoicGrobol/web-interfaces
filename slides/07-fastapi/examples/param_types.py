from fastapi import FastAPI, HTTPException

app = FastAPI()


knights = [
    "King Arthur",
    "Sir Bedevere the Wise",
    "Sir Lancelot the Brave",
    "Sir Galahad the Chaste",
    "Sir Robin the Not-Quite-So-Brave-As-Sir-Lancelot",
    "Bors",
    "Gawain",
    "Ector",
]


@app.get("/knights/")
async def name(number: int):
    try:
        return {"knight": knights[number]}
    except IndexError as e:
        raise HTTPException(status_code=404, detail=f"No knight with number {number} found") from e
