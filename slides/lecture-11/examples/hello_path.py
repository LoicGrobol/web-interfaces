from fastapi import FastAPI

app = FastAPI()


@app.get("/en")
async def root_en():
    return {"message": "Hello World"}


@app.get("/fr")
async def root_fr():
    return {"message": "Wesh les individus"}