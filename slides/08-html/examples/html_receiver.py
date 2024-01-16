import itertools
import pathlib

from fastapi import FastAPI, Form


app = FastAPI()


@app.post("/")
async def read_message(message: str = Form(...)):
    file_number = next(
        i for i in itertools.count() if not pathlib.Path(f"{i}.txt").exists()
    )
    pathlib.Path(f"{file_number}.txt").write_text(message)
