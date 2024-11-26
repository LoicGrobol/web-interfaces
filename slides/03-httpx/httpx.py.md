---
jupyter:
  jupytext:
    custom_cell_magics: kql
    formats: ipynb,md
    split_at_heading: true
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.2
  kernelspec:
    display_name: cours-web
    language: python
    name: python3
---

<!-- LTeX: language=fr -->

<!-- #region slideshow={"slide_type": "slide"} -->
Cours 3 : utiliser `httpx`
=============================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

<!-- #endregion -->

**Note** La bibliothèque [requests](https://requests.readthedocs.io), un peu moins moderne est aussi
très utilisée, ça peut valoir le coup d'y jeter un œil.

<!-- #region slideshow={"slide_type": "slide"} -->
**Note** Si vos requêtes sur httpbin (qui n'est plus maintenu au 2024-11-26) font des timeouts, vous
pouvez essayer avec `https://httpbingo.org` à la place. Sinon vous pouvez utiliser httpbin en local
(attention, ça ne marchera donc pas sur Binder). Installez-le (dans un venv bien sûr) si besoin (il
est maintenant dans le `requirements.txt` du cours).

```bash
python -m pip install gunicorn httpbin
```

ou avec [uv](https://docs.astral.sh/uv/)

```bash
uv pip install gunicorn httpbin
```

Il se lance ensuite avec

```bash
gunicorn httpbin:app
```

Si vous le laisser tourner dans un terminal, vous pouvez ensuite envoyer vos requêtes à
`http://localhost:8000`. Arrêtez-le avec <kbd>ctrl</kbd>+<kbd>C</kbd>. Voir
<https://github.com/psf/httpbin> pour plus d'info (par exemple comment faire ça avec Docker).

En désespoir de cause, lancez netcat avec `nc -kdl 8000` et faites vos requêtes
`http://localhost:8000`, vos requêtes feront des timeout (netcat ne répond pas), mais au moins vous
les verrez dans le terminal.

<!-- #endregion -->

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
[`httpx`](https://www.python-httpx.org/).

Ce cours est largement inspiré du [tutoriel sur `requests` de RealPython](https://realpython.com/python-requests/#getting-started-with-requests) et du [quickstart de `requests`](https://docs.python-requests.org/en/latest/user/quickstart) (mais adaptés à httpx).

## `httpx` ?

`httpx`.

`httpx` est une bibliothèque développée par [encode](https://www.encode.io/), à qui on doit aussi uvicorn et starlette, dont on reparlera, ainsi que MkDocs, qui est la base d'à peu près la moitié des sites de documentation sérieux.

httpx doit être installé. Si vous avez installé le `requirements.txt` du cours, rien de nouveau. Sinon faites-le en exécutant la cellule ci-dessous (rappellez-vous de toujours travailler dans un environnement virtuel).

```python
%pip install -U httpx[http2]
```

L'extra `[http2]` sert à installer les fonctions liées à HTTP/2, qu'on ne verra en principe pas dans
ce cours mais qui peuvent être utiles. Si vous voulez aussi l'interface en ligne de commande (un
genre de cURL), vous pouvez installer avec `[cli]`, ou `[http2, cli]` pour avoir les deux.

```python
import httpx
```

## Une première requête

Exécutez la cellule de code suivante

```python
httpx.get("https://plurital.org")
```

Bravo, vous avez fait votre première requête HTTP en Python ! La fonction `httpx.get` envoie en effet une requête `GET` à l'URL passée en argument.

Bon, par contre la réponse affichée n'est pas très informative.

### L'objet `Response`

On recommence

```python
response = httpx.get("https://plurital.org")
type(response)
```

`httpx.get` renvoie donc un objet du type [`httpx.Response`](https://www.python-httpx.org/api/#response), qui est une interface pour le contenu de la réponse HTTP obtenue. Nous allons voir ses principales propriétés.

#### `status_code`

```python
response.status_code
```

La valeur de `response.status_code` est la valeur du code d'état de la réponse HTTP. Les plus important pour nous sont

- [`200 OK`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/200) : la requête a réussi et si des données ont été demandées, elles seront dans le corps de la réponse.
- [`404 NOT FOUND`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404) : la ressource demandée n'a pas été trouvée. Souvent parce que le serveur ne trouve pas de ressource à l'adresse demandée.

→ Voir [la liste complète sur MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

```python
httpx.get("http://example.com/this/resource/does/not/exist")
```

On peut vérifier si une requête est un succès avec `is_success`

```python
for url in (
    "https://plurital.org",
    "https://example.com/this/resource/does/not/exist",
):
    response = httpx.get(url).raise_for_status()
    if response.is_success:
        print(f"{url} est atteignable")
    else:
        print(f"{url} n'est pas atteignable ")
```

Si on veut lever une exception en cas d'erreur, on peut aussi utiliser `raise_for_status()` :

```python
for url in (
    "https://plurital.org",
    "https://example.com/this/resource/does/not/exist",
):
    try:
        response = httpx.get(url).raise_for_status()
    except httpx.HTTPStatusError as e:
        print(f"{url} n'est pas atteignable : {e}")
        continue
    print(f"{url} est atteignable")
```

**Attention** `200` n'est pas le seul code correspondant à une réussite.

### Contenu

Une requête de type `GET` attend en général une ressource, qui se trouve en cas de succès dans le contenu ou *payload* de la réponse.

S'il s'agit d'un texte, on le trouvera dans l'attribut `text`

```python
response = httpx.get("https://plurital.org")
print(response.text)
```

Dans le cas de la page d'accueil du site du master, il est assez conséquent, puisqu'il s'agit de tout le code HTML de la page.

`httpx` fait de son mieux pour déterminer automatiquement l'encodage du texte, mais s'il se trompe, le contenu sous forme binaire non décodée est toujours disponible dans l'attribut `content`.

```python
print(response.content)
```

Et on peut le décoder explicitement

```python
import codecs
print(codecs.decode(response.content, "cp1252")[-100:])
```

```python
# TODO: un exemple avec une image
```

### Headers

On a dit que les *headers* des messages HTTP contiennent des métadonnées sur ces messages. Le header de notre réponse est accessible directement sous forme de dictionnaire.

```python
response.headers
```

## Les autres types de requêtes

On peut de la même façon faire des requêtes `PUT` et `POST` (ainsi que toutes les autres d'ailleurs).

```python
response = httpx.post("https://httpbin.org/post")
print(response.text)
```

```python
response = httpx.put("https://httpbin.org/put")
print(response.text)
```

Ce sont toutes simplement des alias pour `httpx.request` :

```python
httpx.request("GET", "https://httpbin.org/get")
print(response.text)
```

On a dit que les requêtes de ces types étaient en général utilisées pour passer des données via leur corps. On peut faire ça avec le paramètre content

```python
response = httpx.put("https://httpbin.org/put", content="Hello, world")
print(response.text)
```

```python
response = httpx.put("https://httpbin.org/put", content="We are the Knights Who Say “Ni”!")
print(response.text)
```

La valeur passée à `content` sera convertie en flux d'octets (le type `bytes`). S'il s'agit d'une
chaîne de caractères, elle sera encodée en UTF-8 (contrairement à ce que fait `requests` qui
respecte [le standard HTTP/1.1 d'avant
2014](https://www.w3.org/International/articles/http-charset/index.en) et utilise ISO-8859-1 par
défaut). Si besoin vous pouvez encoder vous-même, avec `"hello".encode("cp1252")` par exemple, et
passer dans ce cas le *header* `Content-Type: text/html; charset=windows-1252`.

## Headers et paramètres

En plus du corps d'une requête, il y a d'autres façons de passer des informations : les paramètres et les headers.

### Les paramètres d'URL

Une façon de passer des options dans une requête est de les ajouter à l'URL demandé, par exemple
<http://httpbin.org/get?key=val> a comme paramètre `key`, de valeur `value` et <https://duckduckgo.com/?q=legends+and+latte&ia=web> a comme paramètres `q`, qui vaut `"legends+and+latte"` et `ia` qui vaut `"web"`.

On peut ajouter ces paramètres directement à l'URL qu'on requête, mais ça demande de les encoder
soi-même, ce qui n'est pas très pratique. À la place on peut les confier à `httpx` sous forme
d'un `dict`.

```python
paramètres = {"clé": "valeur", "formation": "Master PluriTAL", "hôtel": "Trivago"}
response = httpx.get("https://httpbin.org/get", params=paramètres)
print(response.text)
```

Voici l'URL qui a été utilisé

```python
response.url
```

### Headers de requêtes

Les *headers* se passent exactement de la même manière, en passant un dictionnaire

```python
response = httpx.get("https://httpbin.org/get", headers={"User-Agent": "pluriquest/1.0.0"})
print(response.text)
```

## 🎨 Exos 🎨

### Une batterie de requêtes

À l'aide de `httpx`, faites les requêtes HTTP suivantes (elles devraient vous dire quelque
chose) :

1. Une requête à <https://httpbin.org>
2. Une requête à <https://httpbin.org/anything>. Que vous renvoie-t-on ?
3. Une requête POST à <https://httpbin.org/anything>
4. Une requête GET à <https://httpbin.org/anything>, mais cette fois-ci avec le paramètre
   `value=panda`
5. Récupérez le fichier `robots.txt` de Google (<http://google.com/robots.txt>)
6. Faites une requête `GET` à <https://httpbin.org/anything> avec le *header* `User-Agent: Elephant`
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
15. Téléchargez la page d'accueil de DuckDuckGo <https://duckduckgo.com> en espagnol (ou une autre
    langue) avec une utilisation judicieuse des *headers*.

### requrl

#### 1. La base

Écrire un **script** `requrl.py`, qui prend comme argument de ligne de commande une URL et affiche la
ressource correspondante sur la sortie standard (comme un curl très très très basique).

#### 2. Quelques paramètres

Ajoutez quelques paramètres à votre commande, vous pouvez utiliser
[`argparse`](https://docs.python.org/3/library/argparse.html), mais je vous recommande plutôt
[`click`](https://click.palletsprojects.com/en/8.0.x/) (qu'il vous faudra installer).

- Ajouter à `requrl` une option `-H`/`--header` qui comme celle de curl permet de passer des headers
  personnalisés.
- Ajouter à `requrl` une option `-o`/`--output` qui comme celle de curl permet d'écrire dans un
  fichier plutôt que sur la sortie standard.
- Ajouter à `requrl` une option `-X`/`--request` qui comme celle de curl permet de choisir le type
  de requête à effectuer parmi `GET`, `PUT` et `POST`, avec `GET` comme valeur par défaut.
- Ajouter à `requrl` une option `-d`/`--data` qui comme celle de curl permet de passer des données
  dans le corps d'une requête `POST`.

Utilisez [httpbin](https://httpbin.com) pour tester votre commande avec ses différentes options.

Vous pouvez aussi essayer d'implémenter les autres options de curl, certaines sont plus faciles que
d'autres.
