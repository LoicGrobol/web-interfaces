from fastapi import FastAPI

app = FastAPI()


@app.get("/en")
async def root():
    return {"message": "Hello World"}


@app.get("/fr")
async def root():
    return {"message": "Wesh les individus"}