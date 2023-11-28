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
async def surname(number):
    try:
        return {"knight": knights[number]}
    except IndexError:
        raise HTTPException(status_code=404, detail=f"No knight with number {number} found")
