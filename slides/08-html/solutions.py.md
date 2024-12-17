---
jupyter:
  jupytext:
    formats: ipynb,md
    split_at_heading: true
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.1
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- LTeX: language=fr -->

<!-- #region slideshow={"slide_type": "slide"} -->
Générer du HTML : solutions
==========================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

<!-- #endregion -->

```python
from IPython.display import display, HTML
```

## 🥋 Exo 🥋

Concevoir

> - Une page HTML avec un formulaire comprenant un champ de texte et un bouton de soumission.
>  Assurez-vous qu'elle passe au [valideur du W3C](https://validator.w3.org)

<!-- #region -->
```html
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="utf-8" />
    <title>Envoyer un message</title>
  </head>
  <body>
    <form action="http://localhost:8000" method="POST">
      <label for="message">Le message à envoyer</label>
      <input name="message" id="message" value="Ni!">
      <button type="submit">Envoyer</button>
    </form>
  </body>
</html>
```
<!-- #endregion -->

> - Une API avec FastAPI qui reçoit des requêtes de type POST venant de la page que vous avez créé
>   et qui crée pour chacune un nouveau fichier texte sur votre machine dont le contenu est le
>   contenu du champ de texte. Vous aurez besoin de regarder [dans sa
>   doc](https://fastapi.tiangolo.com/tutorial/request-forms/) comment on récupère dans FastAPI des
>   données envoyées depuis un formulaire (malheureusement ce n'est pas du JSON ! Pour ça il faut
>   court-circuiter avec du JavaScript).

```python
# %load examples/html_receiver.py
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

```

### 🎈 Exo 🎈

> Écrire une fonction qui prend en argument une liste de chaines de caractères et un chemin vers un
> fichier et qui écrit dans ce fichier une page HTML qui contient une liste non-ordonnée dont les
> éléments sont les chaînes passées en argument.


Bien entendu, vérifiez que votre HTML passe au [valideur du W3C](https://validator.w3.org).

```python
def make_ul(elems: list[str], path: str):
    above = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>What is the Average Flying Speed of an African Sparrow?</title>
  </head>
  <body>
  <ul>
"""
    below = """
  </ul>
  </body>
</html>
"""
    lst  = "\n".join([f"<li>{name}</li>" for name in elems])
    content = "\n".join([above, lst, below])
    with open(path, "w") as out_stream:
        out_stream.write(content)

# Pour tester
make_ul(["The Beths", "Beirut", "Death Cab for Cutie"], "local/moody_bands.html")
print(open("local/moody_bands.html").read())
```

## 🧊 Exo 🧊

> 1\. Concevoir une API avec FastAPI qui reçoit des requêtes de type POST contenant une liste de
> chaînes de caractère et répond avec une page HTML qui contient une liste ordonnée dont les
> éléments sont les chaînes de caractères reçus.
>
> Bien entendu, vérifiez que votre HTML passe au [valideur du W3C](https://validator.w3.org).

```python
# %load examples/echo_list_api.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()


class InputData(BaseModel):
    lines: list[str]


@app.post("/", response_class=HTMLResponse)
async def display(inpt: InputData):
    above = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>This is what you asked me to display</title>
  </head>
  <body>
  <ol>
"""
    below = """
  </ol>
  </body>
</html>
"""
    lst = "\n".join([f"<li>{name}</li>" for name in inpt.lines])
    html_content = "\n".join([above, lst, below])
    return HTMLResponse(content=html_content, status_code=200)
```

> 2\. Reprendre votre API précédente qui utilisait spaCy pour renvoyer les POS tag correspondant à
> une requête et faites lui renvoyer une présentation des résultats en HTML plutôt que du JSON.

```python
# %load examples/spacy_html_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
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
    above = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>This is what you asked me to display</title>
  </head>
  <body>
  <ol>
"""
    below = """
  </ol>
  </body>
</html>
"""
    lst = "\n".join([f"<li>{w.text}: {w.pos_}</li>" for w in doc])
    html_content = "\n".join([above, lst, below])
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/list")
async def list_models():
    return {"models": spacy.util.get_installed_models()}
```

## 🙄 Exo 🙄

Reprenez les APIs de 🧊 et réécrivez-les en Jinja. Si, si, c'est pour votre bien.
