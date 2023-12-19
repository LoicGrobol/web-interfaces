---
jupyter:
  jupytext:
    formats: ipynb,md
    split_at_heading: true
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.0
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- LTeX: language=fr -->

<!-- #region slideshow={"slide_type": "slide"} -->
Cours 3 : utiliser `requests`
=============================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

<!-- #endregion -->

```python
from IPython.display import display
```

**Note (2022-02-06)** La bibliothèque [httpx](https://github.com/encode/httpx) semble être plus à
jour que requests, tout en étant largement compatible. Y jeter un œil serait intéressant.

## HTTP en Python

Python est « *batteries included* », il comprend donc **en théorie** déjà tout ce qu'il faut pour
communiquer en HTTP, aussi bien du point de vue client que serveur. On pourra regarder par exemple
les modules suivants :

- [`http`](https://docs.python.org/3/library/http.html)
- [`urllib`](https://docs.python.org/3/library/urllib.html)
- [`socketserver`](https://docs.python.org/3/library/socketserver.html#)
- [`sockets`](https://docs.python.org/3/library/socket.html)

**MAIS**

Ils sont assez désagréables à utiliser. Ce qui est assez compréhensible : ils sont prévus soit pour
des usages très simples soit pour servir de base à des bibliothèques de plus haut niveau.

On jouera donc peut-être un peu avec plus tard, mais dans un premier temps on va se concentrer sur
une bibliothèque dont l'objectif est de rendre tout ceci simple :
[`requests`](https://docs.python-requests.org).

Ce cours est largement inspiré du [tutoriel sur `requests` de RealPython](https://realpython.com/python-requests/#getting-started-with-requests) et du [quickstart de `requests`](https://docs.python-requests.org/en/latest/user/quickstart).

## `requests` ?

`requests`.

`requests` est un projet de [Kenneth Reitz](https://kennethreitz.org/), un développeur Python très
prolifique et très bon en relations publiques, connu pour le soin apporté aux interfaces de ses
bibliothèques, réputées *simples* et *puissantes*.

(Cela étant dit, je ne vous recommande pas d'utiliser un de ses projets phares, `pipenv`.)

Installons `requests`, soit dans votre terminal avec `pip`, soit en exécutant la cellule de code
suivante. Comme d'habitude, il est vivement recommandé de travailler pour ce cours dans un
[environnement virtuel](../lecture-05/lecture-05.md) et si vous avez installé le
[requirements.txt](../../requirements.txt) de ce cours, `requests` est déjà installé.


```python
%pip install -U requests
```

```python
import requests
```

## Une première requête


Exécutez la cellule de code suivante

```python
requests.get("http://plurital.org")
```

Bravo, vous avez fait votre première requête HTTP en Python ! La fonction [`requests.get`](https://docs.python-requests.org/en/latest/api/#requests.get) envoie en effet une requête `GET` à l'URL passée en argument.

### L'objet `Response`

On recommence

```python
response = requests.get("http://plurital.org")
type(response)
```

[`requests.get`](https://docs.python-requests.org/en/latest/api/#requests.get) renvoie un objet du type [`requests.Response`](https://docs.python-requests.org/en/latest/api/#requests.Response), qui est une interface pour le contenu de la réponse HTTP obtenue. Nous allons voir ses principales propriétés.

#### `status_code`

```python
response.status_code
```

La valeur de `response.status_code` est la valeur du code d'état de la réponse HTTP. Les plus important pour nous sont

- [`200 OK`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/200) : la requête a réussi et si des données ont été demandées, elles seront dans le corps de la réponse.
- [`404 NOT FOUND`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404) : la ressource demandée n'a pas été trouvée. Souvent parce que le serveur ne trouve pas de ressource à l'adresse demandée.

→ Voir [la liste complète sur MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

```python
requests.get("http://example.com/this/resource/does/not/exist")
```

Les objets de type `Response` ont une valeur de vérité intéressante : ils sont vrais si et seulement si la requête a réussi :

```python
for url in (
    "http://plurital.org",
    "http://example.com/this/resource/does/not/exist",
):
    response = requests.get(url)
    if response:
        print(f"{url} est atteignable")
    else:
        print(f"{url} n'est pas atteignable")
```

**Attention** `200` n'est pas le seul type code correspondant à une réussite.

### Contenu

Une requête de type `GET` attend en général une ressource, qui se trouve en cas de succès dans le contenu ou *payload* de la réponse.

S'il s'agit d'un texte, on le trouvera dans lattribut `text`

```python
response = requests.get("http://plurital.org")
response.text
```

Dans le cas de la page d'accueil du site du master, il est asseez conséquent, puisqu'il s'agit de tout le code HTML de la page.


`requests` fait de son mieux pour déterminer automatiquement l'encodage du texte, mais s'il se trompe, le contenu sous forme binaire non décodée est toujours disponible dans l'attribut `content`.

```python
response.content
```

Et on peut le décoder explicitement

```python
import codecs
print(codecs.decode(response.content, "cp1006")[2000:2300])
```

### Headers

On a dit que les *headers* des messages HTTP contiennent des métadonnées sur ces messages. Le header de notre réponse est accessible directement sous forme de dictionnaire.

```python
response.headers
```

## Les autres types de requêtes

On peut de la même façon faire des requêtes `PUT` et `POST` (ainsi que toutes les autres d'ailleurs).

```python
requests.post("https://httpbin.org/post")
```

```python
requests.put("https://httpbin.org/put")
```

On a dit que les requêtes de ces types étaient en général utilisées pour passer des données via leur corps. On peut faire ça avec le paramètre data

```python
requests.put("https://httpbin.org/put", data="Hello, world")
```

N'importe quel type de données

```python
requests.put("https://httpbin.org/put", data="We are the knights who say “Ni”!")
```

Ah.


Quel est le problème ici ?


En fait, `requests` ne sait passer que des paramètres binaires, et il encode implicitement les chaînes de caractères en `latin-1`, [comme c'est la norme](https://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.4.1).


Pour utiliser un autre encodage, il faut le faire à la main.

```python
requests.post("https://httpbin.org/post", data="We are the knights who say “Ni”!".encode("utf-8"))
```

Mais là le serveur ne saura pas deviner que c'est cet encodage que vous utilisez, il faudra encore lui dire via les *headers*.

```python
response = requests.post("https://httpbin.org/post", data="We are the knights who say “Ni”!".encode("utf-8"), headers={'Content-Type': 'text/plain; charset=utf-8'})
response
```

## Headers et paramètres

En plus du corps d'une requête, il y a d'autres façons de passer des informations : les paramètres et les headers.

### Les paramètres d'URL

Une façon de passer des options dans une requête est de les ajouter à l'URL demandé, par exemple <http://httpbin.org/get?key=val> a comme paramètre `key`, de valeur `value`.

On peut ajouter ces paramètres directement à l'URL qu'on requête, mais celà demande de les encoder soi-même, ce qui n'est pas très pratique. À la place on peut les confier à `requests` sous forme d'un dict.

```python
paramètres = {"clé": "valeur", "formation": "Master PluriTAL", "hôtel": "Trivago"}
response = requests.get("https://httpbin.org/get", params=paramètres)
display(response)
```

Voici l'URL qui a été utilisé

```python
response.url
```

### Headers de requêtes

Les *headers* se passent exactement de la même manière, en passant un dictionnaire

```python
response = requests.get("https://httpbin.org/get", headers={"user-agent": "pluriquest/1.0.0"})
display(response.content)
```

Tiens, c'est marrant cette réponse. À quoi ça ressemble ?

## 🎨 Exos 🎨

### Une batterie de requêtes

À l'aide de `requests`, faites les requêtes HTTP suivantes (elles devraient vous dire quelque
chose) :

1. Une requête à <https://httpbin.org>
2. Une requête à <https://httpbin.org/anything>. Que vous renvoie-t-on ?
3. Une requête POST à <https://httpbin.org/anything>
4. Une requête GET à <https://httpbin.org/anything>, mais cette fois-ci avec le paramètre
   `value=panda`
5. Récupérez le fichier `robots.txt` de Google (<http://google.com/robots.txt>)
6. Faites une requête `GET` à <https://httpbin.org/anything> avec le *header* `User-Agent: elephant`
7. Faites une requête à <https://httpbin.org/anything> et affichez les *headers* de la réponse
8. Faites une requête `POST` à <https://httpbin.org/anything> avec comme corps `{"value": "panda"}`
9. Faites la même requête qu'en 8., mais cette fois-ci en précisant en *header* `Content-Type:
   application/json`
10. Une requête GET à <https://www.google.com> avec le *header* `Accept-Encoding: gzip`.
11. Faites une requête à <https://httpbin.org/image> avec le *header* `Accept: image/png`.
    Sauvegarder le résultat dans un fichier PNG et ouvrez-le dans une visualiseuse d'images. 
12. Faites une requête PUT à <https://httpbin.org/anything>
13. Récupérez <https://httpbin.org/image/jpeg>, sauvegardez le résultat dans un fichier et ouvrez le
    dans un éditeur d'images
14. Faites une requête à <https://httpbin.org/anything> en précisant un login et un mot de passe
15. Téléchargez la page d'accueil de Twitter <https://twitter.com> en espagnol (ou une autre langue)
    avec une utilisation judicieuse des *headers*.

### requrl

#### 1. La base

Écrire un script `requrl.py`, qui prend comme argument de ligne de commande une URL et affiche la
ressource correspondante sur la sortie standard (comme un curl très très très basique).

#### 2. Quelques paramètres

Ajoutez quelques paramètres à votre commande, vous pouvez utiliser
[`argparse`](https://docs.python.org/3/library/argparse.html), mais je vous recommande plutôt
[`click`](https://click.palletsprojects.com/en/8.0.x/) (qu'il vous faudra installer).

- Ajouter à `requrl` une option `-H`/`--header` qui comme celle de curl permet de passer des headers
  personnalisés
- Ajouter à `requrl` une option `-o`/`--output` qui comme celle de curl permet d'écrire dans un
  fichier plutôt que sur la sortie standard
- Ajouter à `requrl` une option `-d`/`--data` qui comme celle de curl permet de passer des données
  dans le corps d'une requête `POST`, afficher un message d'erreur si la requête est d'un autre
  type.

Utilisez [httpbin](https://httpbin.com) pour tester votre commande avec ses différentes options.

Vous pouvez aussi essayer d'implémenter les autres options de curl, certaines sont plus faciles que d'autres.
