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
Cours 11 : Faire des API web avec FastAPI
=========================================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

2021-10-13
<!-- #endregion -->

```python
from IPython.display import display
```

## Pitch

Après avoir bien roulé nos bosses du côté client des API web, après avoir lutté contre les
impitoyables codes d'erreurs et conquis à coup de requêtes les page encyclopédiques les plus sales
de la planète, après avoir été des consomateurices sans scrupules ni vergogne, le temps est enfin de
venu de passer l'autre côté du bar et de faire des **serveurs**

😱

Comme d'habitude, Python est là pour nous, prêt à subvenir à tous nos besoins.

Note importante : à partir d'ici on va devoir faire des trucs qui nécessite plus de droits que ce
que nous offre Binder, il va donc plutôt falloir ouvrir ces documents en local, et très vite écrire
des scripts (oui, oui). Donc [maintenant](../lecture-10/lecture-10.md) que vous savez utiliser Git,
cloner <https://github.com/loicgrobol/apprentissage-artificiel> et travailler en local sera
certainement plus pratique.

Nous disions donc que Python était là pour nous : démonstration, exécutez la cellule suivante après avoir commenté sa première ligne.

```script magic_args="false --no-raise-error"
import http.server
import socketserver

with socketserver.TCPServer(("", 8000), http.server.SimpleHTTPRequestHandler) as httpd:
    httpd.serve_forever()
```

et allez à <http://localhost:8000>.


Et maintenant faites Kernel > Interrupt ou tapez `I I` sinon le serveur va tourner à jamais


On pourrait comme d'habitude faire avec les outils de la bibliothèque standard tout ce dont on peut
avoir besoin. Mais comme d'habitude, faire même les choses les plus simples devient très vite très
compliqué. On va donc utiliser la star du jour : FastAPI.

## FastAPI ?

[FastAPI](https://fastapi.tiangolo.com).

FastAPI est une bibliothèque conçue par [Sebastián Ramírez](https://tiangolo.com), un ancien
développeur de chez [Explosion.ai](https://explosion.ai/), une charmante entreprise qui développe
des outils libres de TAL. Vous avez sans doute déjà entendu parler de [spaCy](https://spacy.io/). À
l'heure ou j'écris ces lignes, il a également une moustache fabuleuse.

Le principe de FastAPI est d'être *rapide* (duh), aussi bien à l'écriture qu'à l'usage. De fait,
c'est probablement la bibliothèque la plus compacte du genre. Elle se repose assez lourdement sur
les [annotations de type](https://docs.python.org/3/glossary.html#term-type-hint), ce qui nous fera
l'occasion de les aborder un peu, je vous conseille comme d'habitude vivement [le tutoriel de *Real
Python* à leur sujet](https://realpython.com/python-type-checking). À plus haut niveau, on y recourt
aussi à [pydantic](pydantic-docs.helpmanual.io), une autre très bonne bibliothèque qui surcharge de
façon très pratique les annotations de type standards.

On utilisera aussi beaucoup les
[décorateurs](https://docs.python.org/3/glossary.html#term-decorator) et devinez qui a [un guide
intéressant à ce sujet](https://realpython.com/primer-on-python-decorators/) ?

Ça vous fait pas mal de lecture, mais comme vingt lignes de cours valent mieux qu'un long discours,
si on y allait ?

Ce qui suit est librement inspiré des tutoriels de FastAPI [de sa propre
doc](https://fastapi.tiangolo.com) et de [*Real
Python*](https://realpython.com/fastapi-python-web-apis).

```python
%pip install -U fastapi[all]
```

## Une première API


**Note**: On peut
[techniquement](https://github.com/David-Lor/FastAPI_LightningTalk-Notebook/blob/master/FastAPI.ipynb)
faire tourner FastAPI dans un notebook, mais ce n'est ni très pratique ni très intéressant et ça n'a
pas grand sens.

**Pour exécuter les exemples suivants, il vous faudra les copier-coller dans des
scripts, où les récupérer depuis le dossier [`examples`](examples/)**.

Je répète **ça ne sert à rien d'exécuter les cellules qui commencent par `# %load` dans la suite de ce notebook**.

Par exemple, voici un script pour faire une API très basique.

```python
# %load examples/hello_api.py
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

Vous pouvez le lancer avec [Uvicorn](https://www.uvicorn.org/), qui est le serveur
[ASGI](https://asgi.readthedocs.io) recommandé pour utiliser FastAPI (même si n'importe quel serveur
ASGI, comme [Hypercorn](https://pgjones.gitlab.io/hypercorn) convient). On ne va pas plus rentrer
dans les détails techniques pour cette fois, l'idée ici est que FastAPI décrit comment marche une
API et que Uvicorn l'exécute et la rend disponible.

<!-- #region -->
```bash
cd examples
uvicorn hello_api:app
```
<!-- #endregion -->

Allez à <http://localhost:8000> et contemplez le résultat de votre première API.

## 😌 Exo 😌

1\. Requêtez votre API avec curl. Bravo ! Vous savez maintenant faire des clients **et** des
serveurs. Prenez une minute pour vous auto-congratuler.

2\. Faites plutôt renvoyer un truc utile à votre API, comme le nom de votre prof préféré⋅e ou la
date du jour.

## Des questions ?

Relisez le premier exemple. Est-ce qu'il y a des choses que vous voyez pour la première fois ?
Est-ce que vous avez des questions ? C'est le moment.

## De la doc ???

Allez à <http://localhost/docs>


C'est beau, hein ?


Parmi les trucs chouettes que FastAPI fait pour nous, il y a un truc très chouette, c'est qu'il
génère automatiquement de la documentation pour nos API.


Pour être précis : il génère une doc au format standard
[OpenAPI](https://spec.openapis.org/oas/latest.html) (dispo à <http://localhost:8000/openapi.json>)
et il lance une interface qui la représente sous le point d'accès `/docs`. Dans cette interface il y
a également un outil pour *tester* vos API, ce qui est **très** pratique. *Try it out* !


(Il y a aussi une interface alternative à [`/redoc`](http://localhost:8000/redoc))


Par défaut la doc est minimaliste (FastAPI ne lisant pas encore dans vos pensées) mais il est très
facile de l'enrichir.

## Et les autres méthodes ?

Easy

```python
# %load examples/hello_post.py
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
```

<!-- #region -->
```bash
cd examples
uvicorn hello_post:app
```
<!-- #endregion -->

```python tags=["raises-exception"]
import requests
requests.post("http://localhost:8000").json()
```

Vous remarquerez que quand on renvoie un `dict`, FastAPI en fait du JSON tout seul comme un grand.
On peut aussi renvoyer d'autres choses (comme du HTML pour faire des pages web 👀) mais ceci est une
autre histoire.

## Est-ce que je peux avoir plusieurs chemins ?

C'est facile, regarde

```python
# %load examples/hello_path.py
from fastapi import FastAPI

app = FastAPI()


@app.get("/en")
async def root_en():
    return {"message": "Hello World"}


@app.get("/fr")
async def root_fr():
    return {"message": "Wesh les individus"}
```

```python tags=["raises-exception"]
requests.get("http://localhost:8000/en").json()
```

```python tags=["raises-exception"]
requests.get("http://localhost:8000/fr").json()
```

## Variables

On peut se servir des chemins pour passer des paramètres à l'API. Par exemple ici pour une base de chevaliers

```python
# %load examples/path_params.py
from fastapi import FastAPI, HTTPException

app = FastAPI()


SURNAMES = {
    "lancelot": "the brave",
    "bedevere": "the wise",
    "galahad": "the chaste",
    "robin": "the not-quite-so-brave-as-sir-lancelot",
    "tim": "the enchanter (not a knight)"
}


@app.get("/knights/{knight_name}")
async def surname(knight_name):
    try:
        return {"surname": SURNAMES[knight_name]}
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Item {knight_name} not found")

```

Remarquez aussi l'utilisation de `HTTPException` qui permet de renvoyer des codes d'erreur HTTP de façon pythonique

```python tags=["raises-exception"]
requests.get("http://localhost:8000/knights/lancelot").json()
```

```python tags=["raises-exception"]
requests.get("http://localhost:8000/knights/mordred").json()
```

Après, c'est plus propre de le faire avec des paramètres de requêtes

```python
# %load examples/query_params.py
from fastapi import FastAPI, HTTPException

app = FastAPI()


SURNAMES = {
    "lancelot": "the brave",
    "bedevere": "the wise",
    "galahad": "the chaste",
    "robin": "the not-quite-so-brave-as-sir-lancelot",
    "tim": "the enchanter (not a knight)"
}


@app.get("/knights/")
async def surname(name):
    try:
        return {"surname": SURNAMES[name]}
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Item {name} not found")

```

```bash tags=["raises-exception"]
curl -X GET "localhost:8000/knights/?name=lancelot"
```

## 💫 Exo 💫

Coder une API qui prend comme paramètres un mot en anglais de la liste de Swadesh et une langue
austronésienne et renvoie le mot correspondant dans cette langue à partir de
[`austronesian_swadesh.csv`](../../data/austronesian_swadesh.csv).

## Conversion de types

Et si j'ai une liste de chevaliers et pas un dict ?

```python
# %load examples/param_types_wrong.py
from fastapi import FastAPI, HTTPException

app = FastAPI()


knights = [
    "King Arthur",
    "Sir Bedevere the Wise",
    "Sir Lancelot the Brave",
    "Sir Galahad the Chaste",
    "Sir Robin the Not-Quite-So-Brave-As-Sir-Lancelot",
    "Bors",
    "Gawain",
    "Ector",
]


@app.get("/knights/")
async def surname(number):
    try:
        return {"knight": knights[number]}
    except IndexError:
        raise HTTPException(status_code=404, detail=f"No knight with number {number} found")

```

```python tags=["raises-exception"]
!curl -X GET "localhost:8000/knights/?number=1"
```

```traceback
return {"knight": knights[number]}
TypeError: list indices must be integers or slices, not str
```


Aïe aïe


Heureusement, c'est bien fait, regardez

```python
# %load examples/param_types.py
from fastapi import FastAPI, HTTPException

app = FastAPI()


knights = [
    "King Arthur",
    "Sir Bedevere the Wise",
    "Sir Lancelot the Brave",
    "Sir Galahad the Chaste",
    "Sir Robin the Not-Quite-So-Brave-As-Sir-Lancelot",
    "Bors",
    "Gawain",
    "Ector",
]


@app.get("/knights/")
async def surname(number: int):
    try:
        return {"knight": knights[number]}
    except IndexError:
        raise HTTPException(status_code=404, detail=f"No knight with number {number} found")

```

```python tags=["raises-exception"]
!curl -X GET "localhost:8000/knights/?number=1"
```

`: int` ici est une *annotation de type* qui signale que `number` devrait être un `int`. En Python,
par défaut, elle n'a pas vraiment d'effet et on pourrait très bien passer autre chose à cette
fonction (c'est surtout initialement prévu pour être lu par vos camarades développeureuses et votre
IDE). Mais FastAPI s'en sert en interne pour convertir automatiquement vers le type demandé.

(on aurait aussi évidemment pu faire la conversion à la main, mais c'est bien pratique comme ça).

```python tags=["raises-exception"]
!curl -X GET "localhost:8000/knights/?number=spam"
```

## Récupérer le corps de la requête


OK, on a vu comment travailler avec les paramètres, mais comment on fait si on veut récupérer des données envoyées dans le corps de la requête ?

Rappellez vous

```python
response = requests.post("https://httpbin.org/post", json={"message": "We are the knights who say “Ni”!"})
response.json()
```

Pour récupére les corps d'une requête dans FastAPI, il faut passer par un modèle [`pydantic`](https://pydantic-docs.helpmanual.io/).

<small>Ça fait une dépendance de plus par rapport à d'autres bibliothèques, mais à la longue ça simplifie les choses, promis</small>

```python
# %load examples/body_api.py
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


# On déclare le format que doivent suivre le corps des requêtes sur notre endpoint
class EchoData(BaseModel):
    message: str


@app.post("/echo")
async def surname(data: EchoData):
    return {"answer": f"Vous avez envoyé le message {data.message!r}"}
```

```python
response = requests.post("http://localhost:8000/echo", json={"message": "We are the knights who say “Ni”!"})
response.json()
```

Pas si compliqué n'est-ce pas ?


Et si on ne suit pas le format ?

```python
response = requests.post("http://localhost:8000/echo", json={"speech": "We are the knights who say “Ni”!"})
display(response)
display(response.json())
```

Ça nous répond bien qu'il y a une erreur. 

## Pydantic et les dataclasses


Les classes comme `EchoData` sont ce qu'on appelle des *dataclasses*, ce sont des nouvelles
arrivantes en Python (3.7+), où elle servent à modéliser des objets qui sont principalement des
conteneurs de données structurées et pour lesquelles le constructeur (`__init__`) peut être
construit automatiquement. Le module natif
[`dataclass`](https://docs.python.org/3/library/dataclasses.html) en propose une implémentation
basique

```python
from dataclasses import dataclass

@dataclass
class DataClassCard:
    rank: str
    suit: str
        
c = DataClassCard(rank="roi", suit="💗")
display(c)
display(c.suit)
```

C'est plus agréable à écrire et utiliser que

```python
class RegularCard:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

c = RegularCard(rank="roi", suit="💗")
display(c)
display(c.suit)
```

On ne rentrera pas dans beaucoup plus de détails sur les dataclasses, mais il y a [des bons
tutos](https://realpython.com/python-data-classes), n'hésitez pas à aller les voir, ça rendra votre
code Python plus doux. 


Ce que propose Pydantic c'est une implémentation alternative des dataclasses, qui offre plus de
possibilités, en se reposant par sur des annotations de type plus riche. FastAPI est capable d'en
tirer parti pour rendre l'écriture d'API plus agréable et pour gérer automatiquement la validation
des données. Là encore on ira pas beaucoup plus loin, mais lisez la doc, suivez le tuto, vous
connaissez la chanson.

## 🪐 Exo 🪐

Écrire une API accessible par POST, qui prend comme paramètre un nom de modèle spaCy et une phrase
et renvoie la liste des POS tags prédits par ce modèle spaCy pour cette phrase.
