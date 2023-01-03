---
jupyter:
  jupytext:
    formats: ipynb,md
    split_at_heading: true
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- #region slideshow={"slide_type": "skip"} -->
<!-- LTeX: language=fr -->
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
Faire des API web avec FastAPI : solutions
==========================================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

<!-- #endregion -->

```python
from IPython.display import display
```

<!-- #region slideshow={"slide_type": "slide"} -->
## 😌 Exo 😌

1\. Requêtez votre API avec curl. Bravo ! Vous savez maintenant faire des clients **et** des
serveurs. Prenez une minute pour vous auto-congratuler.
<!-- #endregion -->
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
```bash
curl http://localhost:8000
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
2\. Faites plutôt renvoyer un truc utile à votre API, comme le nom de votre prof préféré⋅e ou la
date du jour.
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
# %load examples/hello_prof.py
import datetime

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": f"Bonjour Morgan, on est le {datetime.date.today()}"}

```


<!-- #region slideshow={"slide_type": "slide"} -->
## 💫 Exo 💫

Coder une API qui prend comme paramètres un mot en anglais de la liste de Swadesh et une langue
austronésienne et renvoie le mot correspondant dans cette langue à partir de
[`austronesian_swadesh.csv`](../../data/austronesian_swadesh.csv).
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
# %load examples/swadesh_api.py
import csv

from fastapi import FastAPI, HTTPException

app = FastAPI()


with open("../data/austronesian_swadesh.csv") as csvfile:
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

```

```python slideshow={"slide_type": "subslide"}
!curl "http://localhost:8000?word=bird&lang=Ilocano"
```

<!-- #region slideshow={"slide_type": "slide"} -->
## 🪐 Exo 🪐

Écrire une API qui avec

- Un point d'accès accessible par GET qui renvoie la liste des modèles spaCy installés
- Un point d'accès accessible par POST, qui prend comme paramètre un nom de modèle spaCy et comme
  données une phrase et renvoie la liste des POS tags prédits par ce modèle spaCy pour cette phrase.
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
# %load examples/spacy_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import spacy

app = FastAPI()


class InputData(BaseModel):
    sentence: str


@app.post("/postag")
async def postag(inpt: InputData, model="fr_core_news_sm"):
    if model not in spacy.util.get_installed_models():
        raise HTTPException(status_code=422, detail=f"Model {model!r} unavailable")
    nlp = spacy.load(model)
    doc = nlp(inpt.sentence)
    return {"tags": [w.pos_ for w in doc]}


@app.get("/list")
async def list_models():
    return {"models": spacy.util.get_installed_models()}
```

```python
!python -m spacy download en_core_web_sm
!python -m spacy download fr_core_news_sm
```

```python slideshow={"slide_type": "subslide"}
import requests
requests.get("http://localhost:8000/list").json()
```

```python
requests.post("http://localhost:8000/postag", params={"model": "fr_core_news_sm"}, json={"sentence": "je reconnais l'existence du kiwi!"}).json()
```
