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

- Une API avec FastAPI qui reçoit des requêtes de type POST venant de la page que vous avez créé et
  qui crée pour chacune un nouveau fichier texte sur votre machine dont le contenu est le contenu du
  champ de texte. Vous aurez besoin de regarder [dans sa doc](https://fastapi.tiangolo.com/tutorial/request-forms/) comment on récupère dans FastAPI des données envoyées depuis un formulaire (malheureusement ce n'est pas du JSON ! Pour ça il faut court-circuiter avec du JavaScript).

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
with open("local/spam.html", "w") as out_stream:
    out_stream.write(doc)
```

Et voilà on a écrit [du HTML](local/spam.html).

### 🎈 Exo 🎈

Écrire une fonction qui prend en argument une liste de chaines de caractères et un chemin vers un
fichier et qui écrit dans ce fichier une page HTML qui contient une liste non-ordonnée dont les
éléments sont les chaînes passées en argument.

```python
from typing import List

def make_ul(elems: List[str], path: str):
    pass  # À vous de jouer

# Pour tester
make_ul(["AronChupa", "The Sidh", "Måneskin"], "local/earworms_producers.html")
```

Bien entendu, vérifiez que votre HTML passe au [valideur du W3C](https://validator.w3.org).

```python
def make_ul(elems: List[str], path: str):
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
make_ul(["AronChupa", "The Sidh", "Måneskin"], "local/earworms_producers.html")
```

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

```python
# %load examples/echo_list_api.py
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()


class InputData(BaseModel):
    lines: List[str]


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

2\. Reprendre votre API précédente qui utilisait spaCy pour renvoyer les POS tag correspondant à une
requête et faites lui renvoyer une présentation des résultats en HTML plutôt que du JSON.

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

## Les templates avec Jinja

Vous avez dû vous en rendre compte générer du HTML programmatiquement comme ça c'est plutôt pénible :

- Soit on fait en générant des chaînes de caractères à la main, mais c'est pas simple d'être dans
  les clous du valideur.
- Soit on génère avec lxml, mais dans ce cas on doit manipuler des grosses hiérarchies d'objets
  compliqués, c'est vite le bazar.

En plus dans aucun des deux cas on a le confort de

- La coloration syntaxique du HTML
- Une gestion correcte par git
- …

Ce qui serait **bien** ça serait de pouvoir écrire du HTML normalement et en Python de ne faire que changer les parties intéressantes.


Ça tombe bien, il y a des outils pour ça.


Meet [Jinja](https://jinja.palletsprojects.com).

### Jinja ?

Jinja.

```python
%pip install -U Jinja2
```

Jinja est un « moteur de templates » (*template engine*), c'est un genre de `str.format` ou de *f-string*. Voyez plutôt :

```python
from jinja2 import Template
t = Template("Hello {{ something }}!")
t.render(something="World")
```

OK, super mais ça on sait déjà faire, qu'est-ce que ça apporte de plus ?

```python
t = Template("My favorite numbers: {% for n in numbers %} {{n}} {% endfor %}")
t.render(numbers=[2, 7, 1, 3])
```

C'est une boucle for !


À quoi ça sert, et bien par exemple on peut s'en servir pour générer des listes :

```python
t = Template("""My favorite people:
<ul>
{% for p in people %}
<li>{{p.name}}, {{p.position}}</li>
{% endfor %}
</ul>
""")
lst = t.render(
    people=[
        {"name": "Guido van Rossum", "position": "Benevolent dictator for life"},
        {"name": "Ines Montani", "position": "cofounder of explosion.ai"},
        {"name": "Emily Bender", "position": "VP-elect of the Association for Computational Linguistics"},
    ]
)
print(lst)
display(HTML(lst))
```

Petite subtilité : pour se débarrasser des lignes vides intempestives, [on peut utiliser un `-`](https://jinja.palletsprojects.com/en/3.0.x/templates/#whitespace-control)

```python
t = Template("""My favorite people:
<ul>
{% for p in people -%}
<li>{{p.name}}, {{p.position}}</li>
{% endfor -%}
</ul>
""")
lst = t.render(
    people=[
        {"name": "Guido van Rossum", "position": "Benevolent dictator for life"},
        {"name": "Ines Montani", "position": "cofounder of explosion.ai"},
        {"name": "Emily Bender", "position": "VP-elect of the Association for Computational Linguistics"},
    ]
)
print(lst)
```

Il y a d'[autres](https://jinja.palletsprojects.com/en/3.0.x/templates/#list-of-control-structures)
fonctionnalités intéressantes dans les templates Jinja, comme les conditions et les macros. On ne va
pas rentrer dans le détail parce que c'est en général une meilleure idée de faire les traitements
compliqués côté Python, mais elles existent et peuvent être utiles à l'occasion.


Ce qui est plus intéressant pour nous, c'est la possibilité d'écrire nos templates dans des
fichiers. Voici par exemple le contenu de
[`examples/templates/basic.html.jinja`](examples/templates/basic.html.jinja) :

```django
<!DOCTYPE html>
<html lang="en">
<head>
    <title>My favourite people</title>
</head>
<body>
    <h1>My favourite people</h1>
    <ul>
        {% for p in people -%}
            <li>{{p.name}}, {{p.position}}</li>
        {% endfor -%}
    </ul>
</body>
</html>
```


On s'en sert ainsi

```python
from jinja2 import Environment, FileSystemLoader
env = Environment(
    loader=FileSystemLoader("examples/templates"),
)
t = env.get_template("basic.html.jinja")
lst = t.render(
    people=[
        {"name": "Guido van Rossum", "position": "Benevolent dictator for life"},
        {"name": "Ines Montani", "position": "cofounder of explosion.ai"},
        {"name": "Emily Bender", "position": "VP-elect of the Association for Computational Linguistics"},
    ]
)
print(lst)
display(HTML(lst))
```

Ça permet de séparer un peu plus la partie **traitement des données** qui est gérée par cotre code
Python et la partie **affichage** des données qui est gérée en Jinja. En plus, les bons IDE
supportent la syntaxe de Jinja, vous devriez donc au moins avoir de la coloration syntaxique !


Parmi les autres fonctions intéressantes, Jinja permet d'échapper automatiquement le HTML, afin de
se prémunir des injections de code. Par exemple si on reprend l'environnement précédent mais qu'on
change un peu les données

```python
lst = t.render(
    people=[
        {"name": "<strong>Guido</strong> van Rossum", "position": "Benevolent dictator for life"},
        {"name": "Ines Montani", "position": "cofounder of explosion.ai"},
        {"name": "Emily Bender", "position": "VP-elect of the Association for Computational Linguistics"},
    ]
)
print(lst)
display(HTML(lst))
```

Évidemment ici ce n'est pas très grave, mais on peut faire beaucoup de choses avec `<script>` par exemple. Mieux vaut donc éviter

```python
env = Environment(
    loader=FileSystemLoader("examples/templates"),
    autoescape=True,
)

t = env.get_template("basic.html.jinja")
lst = t.render(
    people=[
        {"name": "<strong>Guido</strong> van Rossum", "position": "Benevolent dictator for life"},
        {"name": "Ines Montani", "position": "cofounder of explosion.ai"},
        {"name": "Emily Bender", "position": "VP-elect of the Association for Computational Linguistics"},
    ]
)
print(lst)
display(HTML(lst))
```

## FastAPI et Jinja

Les deux s'interfacent bien, ou plus précisément, FastAPI propose des interfaces vers Jinja


Voici le contenu de [`examples/templates/hello.html.jinja`](examples/templates/jinja_api.py)

```django
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Hello, {{name}}</title>
</head>
<body>
    <h1>Hello, {{name}}</h1>
    <p>How do you do, fellow nerd?</p>
</body>
</html>
```


Et de [`examples/jinja_api.py`](examples/jinja_api.py)

```python
# %load examples/jinja_api.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# Le paramètre `request` est obligatoire, c'est la faute à Starlette !
@app.get("/hello/{name}", response_class=HTMLResponse)
async def read_item(request: Request, name: str):
    return templates.TemplateResponse(
        "hello.html.jinja", {"request": request, "name": name}
    )

```

Lancez cette API avec `uvicorn jinja_api:app` et allez à <http://localhost:8000/hello/world>


## 🙄 Exo 🙄

Reprenez les APIs de 🧊 et réécrivez-les en Jinja. Si, si, c'est pour votre bien.
