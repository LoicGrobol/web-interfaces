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
Cours 17 : *And another thing…*
===============================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

2021-11-17
<!-- #endregion -->


```python
from IPython.display import display
```

## JavaScript

JavaScript (ou ECMAScript) est un langage de programmation originellement conçu pour être intégré à
des pages web et être interprété par les navigateurs. Ça permet de donner des fonctions dynamiques à
des pages web sans avoir à communiquer avec un serveur distant : JavaScript tourne en local, sur la
machine qui affiche la page.

Depuis, comme les autres technologies du web ses usages se sont considérablement étendues, notamment
via [NodeJS](https://nodejs.org) qui permet de l'utiliser comme un langage de programmation système
ou des plateformes comme [React Native](https://reactnative.dev) ou
[Electron](https://www.electronjs.org) qui permettent de concevoir des interfaces graphiques natives
(qui se passent d'un navigateur) en HTML+JavaScript.

Il sert également de langage de base pour des langages transpilés comme
[TypeScript](https://www.typescriptlang.org) ou [CoffeeScript](https://coffeescript.org).

En général, on utilise assez peu JavaScript seul, en partie parce qu'il était historiquement (disons
avant sa version 6) assez idiosyncratique et plutôt désagréable à utiliser, des efforts sont fait
depuis et ça va de mieux en mieux. On continue quand même à utiliser des boîtes à outils
comme [JQuery](https://jquery.com/), qui

- Servent de complément à la bibliothèque standard
- Peuvent être mis à jour régulièrement sans nécessiter de mise à jour des navigateurs clients

Mais le besoin n'est plus aussi crucial qu'il l'a été, suite à l'introduction des API [`fetch`](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) et [Selectors](https://www.w3.org/TR/selectors-api).

Pour faire des pages web dynamiques, au delà de cas simples, je vous recommande l'utilisation de
frameworks comme [React](https://reactjs.org) ou [Angular](https://angular.io).

## Gotchas

Il y a énormément à dire et à apprendre au-delà de ce cours, et je vous recommande très fortement
d'aller lire, ou au moins picorer [le tutoriel de
MDN](https://developer.mozilla.org/en-US/docs/Learn/JavaScript) et le [*Modern Javascript
Tutorial*](https://javascript.info). 

Ici, on va se limiter à quelques trucs bons à savoir si vous apprenez JavaScript en venant de Python

### Instructions et fins de lignes

<!-- #region -->
Les instructions sont séparées comme en Python par des fins de ligne s'il n'y a pas d'ambiguïté

```javascript
console.log("machin")
console.log("truc")
```

On peut aussi les mettre sur une même ligne, comme en Python, en les séparant par des `;` **mais on évite**

```javascript
console.log("machin"); console.log("truc")
```

En revanche on met un `;` quand il s'agit de lever une ambiguïté :

```javascript
const a = 2
const b = 3
(a + b).toString()
```

Ne fait pas ce que vous pensez mais 

```javascript
const a = 2
const b = 3(a + b).toString()
```

Ce qui est une erreur. Il faut plutôt écrire

```javascript
const a = 2
const b = 3;
(a + b).toString()
```

ou mon préféré

```javascript
const a = 2
const b = 3
;(a + b).toString()
```
<!-- #endregion -->

### Blocs et accolades

<!-- #region -->
Contrairement à Python (mais comme beaucoup de langages), en JavaScript, on délimite les blocs non
pas avec des tabulations mais avec des accolades :

```javascript
const t = [1, 2, 3, 4, 5]
for (const v of t){
    if (v > 2){
        console.log(v)
    } else {
        console.log(v+1)
    }
}
```

Vous pouvez faire ce que vous voulez avec l'indentation, ça marchera, mais on recommande en général
d'indenter dans les blocs comme vous en avez l'habitude.
<!-- #endregion -->

### Déclarer des variables


Les variables se **déclarent** à leur première utilisation avec `let` ou `const` (pour les rendre
constantes) ou avec `var` **mais éviter d'utiliser `var`** qui tend à devenir obsolète

<!-- #region -->
La portée d'une variable, c'est le bloc dans lequel elle est définie, ainsi

```javascript
const a = 2
if (a != 2) {
    let x = 1
} else {
    let x = 2
}
console.log(x)
```

renverra une erreur à la dernière ligne : `x` n'est pas définie en dehors du bloc. Il faut plutôt
écrire

```javascript
const a = 2
let x
if (a != 2) {
    x = 1
} else {
    x = 2
}
console.log(x)
```
<!-- #endregion -->

### Boucles for

Pour des raisons historiques, il y a trois types de boucles `for` en `JavaScript`

- `for` qui est la boucle `for` du langage C :

  ```javascript
  let str = "";

  for (let i = 0; i < 9; i++) {
      str = str + i;
  }

  console.log(str);
  ```

  (notez l'affreuse conversion implicite entre entier et chaîne de caractères)
- `for (… of …)` qui plus ou moins la même chose que `for` en Python

  ```javascript
  const array1 = ['a', 'b', 'c'];

  for (const element of array1) {
      console.log(element);
  }
  ```

- `for (… in …)` qui est une abomination, une erreur du passé que vous ne voulez pas utiliser, allez
  lire [la doc](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Statements/for...in)
  pour frémir d'horreur.

<!-- #region -->
### Fonctions

Il y a deux façons de définir des fonctions en JavaScript :

- L'historique [déclaration `function`](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Statements/function) et son jumeau le [mot-clé `function`](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Operators/function)

  ```javascript
  function getRectArea(width, height) {
    return width * height;
  };
  ```

  ```javascript
  const getRectArea = function(width, height) {
    return width * height;
  };
  ```

- Les modernes fonctions fléchées

  ```javascript
  const getRectArea = (width, height) => {
    return width * height;
  };
  ```

Il y a des [différences parfois subtiles entre les
deux](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions).
En général on utilise surtout les fonctions fléchées pour des fonctions anonymes (comme les lambdas
en Python, mais ici elles ne sont pas limitées à une seule expression)

```javascript
const materials = [
  'Hydrogen',
  'Helium',
  'Lithium',
  'Beryllium'
];

console.log(materials.map(material => material.length));
```
<!-- #endregion -->

<!-- #region -->
### DOM et usage dans un navigateur

En général on utilise JavaScript dans une page web. Dans ce cas, il existe un objet global,
`document` qui est une représentation de la page et de ses éléments et qui offre un grand nombre
d'outils pour les observer et les manipuler. Par exemple ceci change la couleur du fond de la page

```javascript
document.body.style.background = "red";
```

On parle de DOM : _**D**ocument **O**bject **M**odel_.

Il **faut** garder sous la main [la documentation du DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model).
<!-- #endregion -->

### Évènements

Beaucoup d'éléments d'interaction en JavaScript utilisent la notion d'évènement, qu'on exploite en
liant des fonctions (`callbacks`) à des actions ou des circonstances prédéfinies (`hooks`)

<!-- #region -->
```html
<input id="elem" type="button" value="Click me">
<script>
  elem.addEventListener(
    "click",
    function() {
        console.log("Hello, world!")
    },
  )
</script>
```
<!-- #endregion -->

`Hello, world!` s'affiche dans la console à chaque fois qu'on clique sur le bouton et seulement à ce
moment (pas au chargement de la page).

Pour des cas simples on peut aussi redéfinir complètement l'évènement

<!-- #region -->
```html
<input id="elem" type="button" value="Click me">
<script>
  elem.onclick = function() {
      alert('Thank you')
  }
</script>
```
<!-- #endregion -->

## Interfaces

En ce qui nous concerne, comme l'objectif est de réaliser des interfaces pour des systèmes de TAL et
étant donné ce qu'on a vu dans ce cours, l'idéal est probablement de ne pas faire reposer trop de
logique sur JavaScript, que ce soit côté client (donc page web) que du côté serveur, je vous
recommande même d'éviter ici d'utiliser du JavaScript côté serveur (ce qu'on pourrait faire en
Node). L'architecture adaptée si vous voulez une interface web graphique :

```
Système de TAL ⇆ API (FastAPI[+Jinja][+SQL]) ⇆ Page web (HTML+CSS+JavaScript)
```

Ici la page web requête l'API au moyen de méthodes comme
[`fetch`](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API). En voici un exemple :

<!-- #region -->
```html
<!DOCTYPE html>
<html lang="fr">

<head>
  <meta charset="utf-8" />
  <title>POS-tagger</title>
</head>

<body>
  <h1>POS-tagger</h1>
  <form action="http://localhost:8000/postag" method="POST" id="inputForm">
    <label for="sentence">La phrase à analyser</label>
    <input name="sentence" id="sentence" value="Il y a un lama dans mon salon !" />
    <button type="submit">Envoyer</button>
  </form>

  <div id="result"></div>
</body>
<script>
  document.querySelector("#inputForm").onsubmit = async (event) => {
      event.preventDefault()
      const form = event.target

      const data = {
          sentence: form.querySelector("#sentence").value,
      }

      // On pourrait aussi utiliser `form.action` plutot que de remettre
      // l'URL en dur
      const response = await fetch(
          "http://localhost:8000/postag",
          {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(data),
          },
      )

      const text = await response.text() // read response body as text
      document.querySelector("#result").innerHTML = text
  }
</script>
</html>
```
<!-- #endregion -->

Elle permet d'accéder à l'API spacy suivante :

```python
# %load apis/spacy_html_api.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import spacy

app = FastAPI()


app.mount("/front", StaticFiles(directory="static"), name="front")


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

<!-- #region -->
Pour le rendu, aller dans le dossier [apis](apis/) qui accompagne ce notebook, lancer l'API dans Uvicorn

```bash
uvicorn spacy_html_api:app
```

puis aller à <http://localhost:8000/front/spacy_api.html>.
<!-- #endregion -->
