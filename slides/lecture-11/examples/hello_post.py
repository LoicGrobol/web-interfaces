from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/")
async def root_post():
    return {
        "message": (
            "you POST api? you post her <body> like the webpage?"
            " oh! oh! jail for server! jail for server for One Thousand Years!!!!"
        ),
    }