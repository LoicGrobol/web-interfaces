from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


# On déclare le format que doivent suivre le corps des requêtes sur notre endpoint
class EchoData(BaseModel):
    message: str


@app.post("/echo")
async def surname(data: EchoData):
    return {"answer": f"Vous avez envoyé le message {data.message!r}"}