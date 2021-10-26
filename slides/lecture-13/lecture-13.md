---
jupyter:
  jupytext:
    formats: ipynb,md
    split_at_heading: true
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.0
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- LTeX: language=fr -->

<!-- #region slideshow={"slide_type": "slide"} -->
Cours 13 : Générer du HTML
==========================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

2021-10-20
<!-- #endregion -->

```python
from IPython.display import display, HTML
```

## HTML

Tutoriels interactifs sur [MDN Learn](https://developer.mozilla.org/en-US/docs/Learn) (ils sont
aussi disponibles en français)

- [*Getting started with
  HTML*](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Getting_started)
- [*Web forms*](https://developer.mozilla.org/en-US/docs/Learn/Forms)
  - Il n'est pas forcément nécessaire de s'attarder trop longtemps sur les questions de style ou les
    contrôles avancé, l'objectif est d'arriver jusqu'à [*Sending and retrieving form
    data*](https://developer.mozilla.org/en-US/docs/Learn/Forms/Sending_and_retrieving_form_data)
- Ne pas hésiter à fouiller dans les autres parties du tutoriel (notamment CSS et JavaScript) pour
  mieux les comprendre. À faire selon vos goûts.

## 🥋 Exo 🥋

Concevoir

- Une page HTML avec un formulaire comprenant un champ de texte et un bouton de soumission.
  Assurez-vous qu'elle passe au [valideur du W3C](https://validator.w3.org)
- Une API avec FastAPI qui reçoit des requêtes de type POST venant de la page que vous avez créé et
  qui crée pour chacune un nouveau fichier texte sur votre machine dont le contenu est le contenu du
  champ de texte.

## Générer du HTML en Python

**En général** quand on crée un service web, on a envie de lui donner une **interface web** lisible
par des humain⋅e⋅s. Autrement dit une page web.


C'est bien gentil de lire du JSON dans un navigateur mais au bout d'un moment ça va bien.

On a vu comment récupérer des informations envoyées par l'utilisateur avec des formulaires,
maintenant on va voir comment lui répondre en affichant des données générées par notre programme.

Il va donc nous falloir *générer du HTML en Python*

### À la main

C'est-à-dire que HTML c'est du texte. Des chaînes de caractères donc.

Du coup vous pouvez en générer en Python, ça va, on sait faire.

```python
doc = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>What is the Average Flying Speed of an African Sparrow?</title>
  </head>
  <body>
    <h1>What is the Average Flying Speed of an African Sparrow?</h1>
    <p>The airspeed velocity of an unladen swallow is something like 20.1 miles per hour or 9 meters per second</p>
  </body>
</html>
"""
print(doc)
```

En plus dans un notebook ça se fait bien avec
[`IPython.display.HTML`](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html#IPython.display.HTML)

```python
HTML(doc)
```

Et vous savez comment écrire dans un fichier

```python
with open("spam.html", "w") as out_stream:
    out_stream.write(doc)
```

Et voilà on a écrit [du HTML](spam.html).

### 🎈 Exo 🎈

Écrire une fonction qui prend en argument une liste de chaines de caractères et un chemin vers un
fichier et qui écrit dans ce fichier une page HTML qui contient une liste non-ordonnée dont les
éléments sont les chaînes passées en argument.

```python
from typing import List

def make_ul(elems: List[str], path: str):
    pass  # À vous de jouer

# Pour tester
make_ul(["AronChupa", "The Sidh", "Måneskin"], "earworms_producers.html")
```

Bien entendu, vérifiez que votre HTML passe au [valideur du W3C](https://validator.w3.org).

### Avec `lxml`

lxml propose une interface sympa pour générer du HTML en étant sûr⋅e de ne pas faire d'erreurs de syntaxe

```python
import lxml
from lxml.html import builder as E
html = E.HTML(
    E.HEAD(
        E.META(charset="utf-8"),
        E.TITLE("What is the Average Flying Speed of an African Sparrow?")
    ),
    E.BODY(
        E.H1("What is the Average Flying Speed of an African Sparrow?"),
        E.P("The airspeed velocity of an unladen swallow is something like 20.1 miles per hour or 9 meters per second"),
    )
)

print(lxml.html.tostring(html, encoding=str))
```

## Avec FastAPI

Pour afficher du HTML quand on accède à votre point d'accès FastAPI, vous pouvez utiliser `fastapi.responses.HTMLResponse`.

```python
# %load examples/html_api.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_items():
    html_content = """
    <html>
        <head>
            <title>What is the Average Flying Speed of an African Sparrow?</title>
        </head>
        <body>
            <h1>What is the Average Flying Speed of an African Sparrow?</h1>
            <p>The airspeed velocity of an unladen swallow is something like 20.1 miles per hour or 9 meters per second</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
```

## 🧊 Exo 🧊


1\. Concevoir une API avec FastAPI qui reçoit des requêtes de type POST contenant une liste de
chaînes de caractère et répond avec une page HTML qui contient une liste ordonnée dont les éléments
sont les chaînes de caractères reçus.

Bien entendu, vérifiez que votre HTML passe au [valideur du W3C](https://validator.w3.org).

2\. Reprendre votre API précédente qui utilisait spaCy pour renvoyer les POS tag correspondant à une
requête et faites lui renvoyer une présentation des résultats en HTML plutôt que du JSON.