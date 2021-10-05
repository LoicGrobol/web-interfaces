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

[comment]: <> "LTeX: language=fr"

<!-- #region slideshow={"slide_type": "slide"} -->
Cours 9 : consommer des API web
================================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

2021-10-06
<!-- #endregion -->

```python
from IPython.display import display
```

```python
%pip install -U requests
```

Ce cours est partiellement adapté du tutoriel [Python and REST
APIs](https://realpython.com/api-integration-in-python/) de Real Python.

## API ?

_**A**plication **P**reogramming **I**nterface_, en français parfois « interface de programmation
d’applications » mais surtout API \[eɪpiˈaɪ\]. À ne pas confondre avec
l'[API](https://www.internationalphoneticalphabet.org) des phonéticiens (puisqu'en anglais, c'est
l'IPA, à ne pas confondre avec les bières enrichies en houblon \[vous suivez ?\]).

Il s'agit d'*interfaces* de communications entre *applications*. À la différence des interfaces
humain⋅e⋅s – machines (même si les deux classes ne sont pas disjointes, d'ailleurs est-ce que vous
voyez des exemples qui sont les deux ?). Autrement dit, une API c'est la surface d'une application,
son panneau de commande accessible par d'autres applications. On suppose en général que ces
interfaces sont

- Publiques
- Documentées
- Stables
- Opaques

Le dernier point, l'*opacité* rejoint les considérations de séparation des préoccupations qu'on a
déjà abordées plusieurs fois : quand j'accède à une application via son API, je ne veux pas avoir à
me soucier de ce qui ce passe en interne. Tout ce qui compte pour moi, c'est ce que j'y mets et ce
que j'en récupère.

Point vocabulaire : si une application A utilise l'API d'une application B, on dira que A est le
*client* et B le *serveur*.

## APIs web

Une API web, c'est une API à laquelle on accède via le web.

Voilà, le cours est fini, joyeux Noël.

En pratique, on parle d'API web quand des services applicatifs sont accessible via des requêtes
HTTP. Par exemple celle de GitHub, à laquelle on accède à <https://api.github.com>. Regardez ce qui
se passe par exemple avec une requête `GET` sur le point d'accès (*endpoint*)
<https://api.github.com/users/loicgrobol>

```python
!curl https://api.github.com/users/loicgrobol
```

```python
requests.get("https://api.github.com/users/loicgrobol")
```

Le serveur est alors littéralement un serveur web, les concepts s'alignent !

Le fait de passer par HTTP pour faire communiquer des applications a bien des avantages :

- On peut communiquer via Internet (HTTP est prévu pour ça) entre machines très distantes
- On peut bénéficier de toutes les technologies et infrastructures développées pour le web
  (matérielles, logicielles et humaines) qui du fait de leur omniprésence sont très optimisées
- HTTP propose tout un tas d'outils intéressants
  - Les URL avoir des chemins d'accès hiérarchisés
  - Les systèmes d'authentification (sessions, cookies…)
  - La transmission bidirectionnelle de données arbitraires (via les *payloads*)

## REST

_**Re**presentational **s**tate **t**ransfer_ est une méthodologie de conception d'API web, pensée
pour demander le moins de *couplage* possible entre une application client et le serveur à l'API
duquel elle accède. Autrement dit le client n'a besoin que très peu de connaissance du
fonctionnement du serveur et vice-versa.

Les principes (un peu simplifiés) de REST sont

- L'absence de mémoire (*statelessness*) : le serveur ne doit pas garder en mémoire de trace des
  requêtes du client.
- La séparation du client et du serveur : les deux doivent être suffisament découplés pour pouvoir
  être modifiés sans conséquence de l'un sur l'autre (tant que l'API ne change pas)
- La possibilité de mettre les requêtes en cache (*cacheability*) : les données renvoyées pour une
  requête données doivent être rigoureusement identique d'une requête sur l'autre afin que le client
  comme le serveur puissent les stocker en mémoire cache.
- L'uniformité des interfaces :
  - L'identification des ressources se fait par un identifiant indépendant de leurs représentations
  - La représentation d'une ressource doit être suffisante pour la mettre à jour ou la supprimer du
    serveur
  - Chaque message doit contenir une description de la façon dont il doit être lu
- L'indépendance d'accès (*layered system*) : le comportement de l'interface doit être identique
  quel que soit le moyen utilisé pour y accéder. En particulier, il ne doit pas changer si cet accès
  passe par des *proxy*.

## Accéder à des API

On l'a déjà fait [plein](../lecture-06/lecture-06.md) de [fois](../lecture-07/lecture-07.md) !

On a dit qu'il suffisait de faire des requêtes HTTP et ça on sait déjà faire :

```python
requests.get("https://jsonplaceholder.typicode.com/todos/1").text
```

Par contre, on a pas reparlé de ce format étrange.

Ça ressemble à la représentation d'un `dict`


```python
dict(requests.get("https://jsonplaceholder.typicode.com/todos/1").text)
```

Mais ce n'est pas tout à fait ça

```python
dict(requests.get("https://api.github.com/users/loicgrobol").text)
```

## JSON

_**J**ava**s**cript **O**bject **N**otation_. Comme son nom l'indique c'est la syntaxe pour noter des objets en Javascript.

C'est très très très proche de la syntaxe des `dict` litéraux en Python. Sauf quand c'est différent.