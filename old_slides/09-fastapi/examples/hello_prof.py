import datetime

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": f"Bonjour Morgan, on est le {datetime.date.today()}"}
