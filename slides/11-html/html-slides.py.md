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
Cours 10 : Générer du HTML
==========================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

<!-- #endregion -->

```python slideshow={"slide_type": "-"}
from IPython.display import display, HTML
```

<!-- #region slideshow={"slide_type": "slide"} -->
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
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
## 🥋 Exo 🥋

Concevoir

- Une page HTML avec un formulaire comprenant un champ de texte et un bouton de soumission.
  Assurez-vous qu'elle passe au [valideur du W3C](https://validator.w3.org)
- Une API avec FastAPI qui reçoit des requêtes de type POST venant de la page que vous avez créé et
  qui crée pour chacune un nouveau fichier texte sur votre machine dont le contenu est le contenu du
  champ de texte. Vous aurez besoin de regarder [dans sa
  doc](https://fastapi.tiangolo.com/tutorial/request-forms/) comment on récupère dans FastAPI des
  données envoyées depuis un formulaire (malheureusement ce n'est pas du JSON ! Pour ça il faut
  court-circuiter avec du JavaScript).
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Générer du HTML en Python

**En général** quand on crée un service web, on a envie de lui donner une **interface web** lisible
par des humain⋅e⋅s. Autrement dit une page web.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
C'est bien gentil de lire du JSON dans un navigateur, mais au bout d'un moment ça va bien.

On a vu comment récupérer des informations envoyées par l'utilisateur avec des formulaires,
maintenant on va voir comment lui répondre en affichant des données générées par notre programme.

Il va donc nous falloir *générer du HTML en Python*
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### À la main

C'est-à-dire que HTML c'est du texte. Des chaînes de caractères donc.

Du coup vous pouvez en générer en Python, ça va, on sait faire.
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
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

<!-- #region slideshow={"slide_type": "subslide"} -->
En plus dans un notebook ça se fait bien avec
[`IPython.display.HTML`](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html#IPython.display.HTML)
<!-- #endregion -->

```python
HTML(doc)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Et vous savez comment écrire dans un fichier
<!-- #endregion -->

```python
with open("local/spam.html", "w") as out_stream:
    out_stream.write(doc)
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Et voilà on a écrit [du HTML](local/spam.html).
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
### 🎈 Exo 🎈

Écrire une fonction qui prend en argument une liste de chaines de caractères et un chemin vers un
fichier et qui écrit dans ce fichier une page HTML qui contient une liste non-ordonnée dont les
éléments sont les chaînes passées en argument.
<!-- #endregion -->

```python
from typing import List

def make_ul(elems: List[str], path: str):
    pass  # À vous de jouer

# Pour tester
make_ul(["The Beths", "Beirut", "Death Cab for Cutie"], "local/moody_bands.html")
print(open("local/moody_bands.html").read())
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Bien entendu, vérifiez que votre HTML passe au [valideur du W3C](https://validator.w3.org).

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
### Avec `lxml`

lxml propose une interface sympa pour générer du HTML en étant sûr⋅e de ne pas faire d'erreurs de
syntaxe
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
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

```python
HTML(lxml.html.tostring(html, encoding=str))
```

<!-- #region slideshow={"slide_type": "subslide"} -->
## Avec FastAPI

Pour afficher du HTML quand on accède à votre point d'accès FastAPI, vous pouvez utiliser
`fastapi.responses.HTMLResponse`, ce qui indique par exemple au navigateur qu'il faut interpréter les données reçues comme une page web.
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
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

<!-- #region -->
Comme d'habitude, lancez depuis [`examples/`](examples/) avec 

```sh
uvicorn html_api:app
```

Et allez voir <http://localhost:8000>
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## 🧊 Exo 🧊
<!-- #endregion -->

<!-- #region -->
1\. Concevoir une API avec FastAPI qui reçoit des requêtes de type POST contenant une liste de
chaînes de caractère et répond avec une page HTML qui contient une liste ordonnée dont les
éléments sont les chaînes de caractères reçus.

Bien entendu, vérifiez que votre HTML passe au [valideur du W3C](https://validator.w3.org).


2\. Reprendre votre API précédente qui utilisait spaCy pour renvoyer les POS tag correspondant à
une requête et faites lui renvoyer une présentation des résultats en HTML plutôt que du JSON.

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Les templates avec Jinja

Vous avez dû vous en rendre compte, générer du HTML programmatiquement comme ça c'est plutôt pénible :

- En écrivant des chaînes de caractères à la main, c'est pas simple d'être dans les clous du valideur.
- Avec lxml, on doit manipuler des grosses hiérarchies d'objets compliqués, c'est vite le bazar.

En plus dans aucun des deux cas on a le confort de

- La coloration syntaxique du HTML
- Une gestion correcte par git
- …

Ce qui serait **bien** ça serait de pouvoir écrire du HTML normalement et en Python de ne faire que changer les parties intéressantes.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Ça tombe bien, il y a des outils pour ça.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
Meet [Jinja](https://jinja.palletsprojects.com).
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Jinja ?

Jinja.
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
%pip install -U Jinja2
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Jinja est un « moteur de templates » (*template engine*), c'est un genre de `str.format` ou de *f-string*. Voyez plutôt :
<!-- #endregion -->

```python
from jinja2 import Template 
t = Template("Hello {{ something }}!")
t.render(something="World")
```

<!-- #region slideshow={"slide_type": "subslide"} -->
OK, super mais ça on sait déjà faire
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
something = "World"
f"Hello {something}"
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Du coup, qu'est-ce que ça apporte de plus ?
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
t = Template("My favorite numbers: {% for n in numbers %} {{n}} {% endfor %}")
t.render(numbers=[2, 7, 1, 3])
```

<!-- #region slideshow={"slide_type": "fragment"} -->
C'est une boucle for !
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
À quoi ça sert ? Et bien par exemple on peut s'en servir pour générer des listes :
<!-- #endregion -->

```python
t = Template("""Some interesting people:
<ul>
{% for p in people %}
<li>{{p.name}}, {{p.position}}</li>
{% endfor %}
</ul>
""")
lst = t.render(
    people=[
        {"name": "Guido van Rossum", "position": "Benevolent dictator for life"},
        {"name": "Ines Montani", "position": "Cofounder of explosion.ai"},
        {"name": "Kirby Conrod", "position": "Linguist and scholar"},
    ]
)
```

```python slideshow={"slide_type": "subslide"}
print(lst)
```

```python
display(HTML(lst))
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Petite subtilité : pour se débarrasser des lignes vides intempestives, [on peut utiliser un
`-`](https://jinja.palletsprojects.com/en/3.1.x/templates/#whitespace-control)
<!-- #endregion -->

```python
t = Template("""Some interesting people:
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
        {"name": "Kirby Conrod", "position": "Linguist and scholar"},
    ]
)
print(lst)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Il y a d'[autres](https://jinja.palletsprojects.com/en/3.1.x/templates/#list-of-control-structures)
fonctionnalités intéressantes dans les templates Jinja, comme les conditions et les macros. On ne va
pas rentrer dans le détail parce que c'est en général une meilleure idée de faire les traitements
compliqués côté Python, mais elles existent et peuvent être utiles à l'occasion.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
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
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
On s'en sert ainsi
<!-- #endregion -->

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
        {"name": "Kirby Conrod", "position": "Linguist and scholar"},
    ]
)
print(lst)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Ça permet de séparer un peu plus la partie **traitement des données** qui est gérée par cotre code
Python et la partie **affichage** des données qui est gérée en Jinja.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
En plus, les bons IDE supportent la syntaxe de Jinja, vous devriez donc au moins avoir de la coloration syntaxique !
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Parmi les autres fonctions intéressantes, Jinja permet d'échapper automatiquement le HTML, afin de
se prémunir des injections de code. Par exemple si on reprend l'environnement précédent mais qu'on
change un peu les données
<!-- #endregion -->

```python
lst = t.render(
    people=[
        {"name": "<strong>Guido</strong> van Rossum", "position": "Benevolent dictator for life"},
        {"name": "Ines Montani", "position": "cofounder of explosion.ai"},
        {"name": "Kirby Conrod", "position": "Linguist and scholar"},
    ]
)
print(lst)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Évidemment ici ce n'est pas très grave, mais on peut faire beaucoup de choses avec `<script>` par exemple. Mieux vaut donc éviter ceci
<!-- #endregion -->

```python
env = Environment(
    loader=FileSystemLoader("examples/templates"),
    autoescape=False,
)

t = env.get_template("basic.html.jinja")
lst = t.render(
    people=[
        {"name": "<strong>Guido</strong> van Rossum", "position": "Benevolent dictator for life"},
        {"name": "Ines Montani", "position": "cofounder of explosion.ai"},
        {"name": "Kirby Conrod", "position": "Linguist and scholar"},
    ]
)
print(lst)
```

<!-- #region slideshow={"slide_type": "slide"} -->
## FastAPI et Jinja

Les deux s'interfacent bien, ou plus précisément, FastAPI propose des interfaces vers Jinja
<!-- #endregion -->

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

<!-- #region slideshow={"slide_type": "subslide"} -->
Et de [`examples/jinja_api.py`](examples/jinja_api.py)
<!-- #endregion -->

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


<!-- #region slideshow={"slide_type": "slide"} -->
## 🙄 Exo 🙄

Reprenez les APIs de 🧊 et réécrivez-les en Jinja. Si, si, c'est pour votre bien.
<!-- #endregion -->
