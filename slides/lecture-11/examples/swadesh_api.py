import csv

from fastapi import FastAPI, HTTPException

app = FastAPI()


with open("../../../data/austronesian_swadesh.csv") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
    swadesh_dict = {
        row["English"]: {k: v for k, v in row.items() if k != "N°"} for row in reader
    }


@app.get("/")
async def swadesh(word, lang="English"):
    try:
        word_translations = swadesh_dict[word]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Word {word!r} not found")

    try:
        return word_translations[lang]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Language {lang!r} not found")
