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
Aller jusqu'à « *Philosophy* », version HTML
==================================================================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

2021-10-06
<!-- #endregion -->

```python
from IPython.display import display
```

## Énoncé

> *Wikipedia trivia: if you take any article, click on the first link in the article text not in
> parentheses or italics, **and then repeat**, you will eventually end up at "Philosophy".*
> (alt-text de [xkcd #903](https://xkcd.com/903/))

- Vérifiez sur une page ou deux si c'est vrai
- Écrivez un script qui prend en argument de ligne de commande un nom de page Wikipédia (en anglais,
  sauf si vous aimez l'aventure) et donne le nombre de sauts nécessaire pour arriver à la page
  *Philosophy* ou une erreur si la page en question n'existe pas
- Si vous êtes très déterminé⋅e⋅s, faites un script qui prend en entrée des pages de Wikipédia et
  produit le graphe (orienté) des pages obtenues en suivant à chaque fois le premier lien de chaque
  page, et ce jusqu'à retomber sur une page déjà visitée. On pourra par exemple utiliser
  [NetworkX](https://networkx.org/documentation/latest/reference/drawing.html), un visualiseur
  interactif comme [pyvis](https://pyvis.readthedocs.io/en/latest/tutorial.html), [un wrapper de
  graphviz](https://graphviz.readthedocs.io) ou encore générer directement des fichiers dot.



On va d'abord commencer par jouer un peu avec les données, on fera un script après

## Introduction

On commence par s'assurer qu'on les bons outils

```python
%pip install -U beautifulsoup4 lxml matplotlib requests
```

```python
from bs4 import BeautifulSoup
import lxml
import requests
```

## Premier essai


On part de la page [Algorithmic Bias](https://en.wikipedia.org/wiki/Algorithmic_bias)

```python
url = "https://en.wikipedia.org/wiki/Algorithmic_bias"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
soup
```

On s'intéresse au corps de page

```python
soup.body
```

Et dans le corps de page au premier parragraphe qui contient du texte

```python
first_p = [p for p in soup.body.find_all("p") if p.text and not p.text.isspace()][0]
first_p
```

On récupère le premier lien (pour l'instant sans plus de condition)

```python
first_link = first_p.a
display(first_link)
display(first_link["href"])
```

Attention son `href` est un lien relatif, on va devoir le résoudre

```python
from urllib.parse import urljoin
next_url = urljoin(url, first_link["href"])
next_url
```

On récupère la page suivante

```python
response = requests.get(next_url)
soup = BeautifulSoup(response.text, 'lxml')
soup.title.text
```

(Il y a eu une pseudo-redirection mais pas via une requête HTTP, plutôt via de la cuisine interne à
MediaWiki et [de la sorcellerie](https://developer.mozilla.org/en-US/docs/Web/API/History/pushState)
en Javascript. Du coup, ça c'est passé sans douleur pour nous.)

## 🔄

On recommence

```python
first_p = [p for p in soup.body.find_all("p") if p.text and not p.text.isspace()][0]
first_p
```

On a de la chance : les bandeaux d'info et notices de redirection n'utilisent pas de balise `<p>`.
Ce n'est pas très robuste de se reposer là-dessus, mais comme de toute façon on reparse du HTML
généré (et pas écrit directement), et pas très propre, on ne sera que rarement robustes…


Plutôt que de refaire la même sauce à la mano, on va écrire une fonction

```python
def get_next_url(url):
    """Récupère la page à `url` et revoie l'addresse du premier lien du premier paragraphe"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    # Plutôt que de créer une liste et de jeter tout sauf son premier élément,
    # on fait ça avec un générateur
    first_p = next(p for p in soup.body.find_all("p") if p.text and not p.text.isspace())
    first_link = first_p.a
    return urljoin(url, first_link["href"])
```

On teste

```python
get_next_url(next_url)
```

Et encore

```python
for _ in range(16):
    print(next_url)
    next_url = get_next_url(next_url)
```

On voit que [Latin language](https://en.wikipedia.org/wiki/Latin) nous envoie sur
[Help:IPA/Latin](https://en.wikipedia.org/wiki/Help:IPA/Latin). Ça n'a pas l'air d'être correct.

## Ne pars pas en thèse


Regardons un peu ce que la page a dans le ventre

```python
response = requests.get("https://en.wikipedia.org/wiki/Latin")
soup = BeautifulSoup(response.text, 'lxml')
first_p = next(p for p in soup.body.find_all("p") if p.text and not p.text.isspace())
first_p
```

Le problème a l'air d'être que la condition « lien pas entre parenthèses » n'est pas vérifiée ici.
Pour empêcher ça on va utiliser le critère suivant : un lien est entre parenthèses s'il est précédé
par plus de parenthèses ouvrantes que de parenthèses fermantes. Pour savoir si un lien est entre
parenthèses, on va donc regarder tout le texte avant lui dans le paragraphe et compter les
parenthèses.

```python
# Le type des textes dans bs4
from bs4.element import NavigableString
# On a besoin de préciser `p` parce que ce n'est peut-être pas le parent direct de `a`
def is_between_parentheses(a, p):
    n_open = 0
    for elem in p.descendants:
        if elem is a:
            break
        # On ne compte les parenthèses que dans les textes
        if isinstance(elem, NavigableString):
            n_open += elem.count("(") - elem.count(")")
    # S'il y a plus d'ouvrants que de fermants c'est pas notre problème
    return n_open > 0
```

```python
first_a = next(a for a in first_p.find_all("a") if not is_between_parentheses(a, first_p))
first_a
```

Ça marche !

## I vecchi tag

Un dernier point ce sont les italiques. En examinant le code on trouve l'horreur suivante (qui se
trouve être entre parenthèses donc ici ça ne gêne pas mais ça pourrait l'être dans une autre page.


<!-- #region -->
```html
<p><b>Latin</b> (<i title="Latin-language text" lang="la">latīnum</i>
```
<!-- #endregion -->

Visiblement chez MediaWiki on a pas trop de complexes avec la non-séparation du style et du contenu
et pour mettre en italiques on utilise `<i>` (ça ne concerne pas les bandeau d'info qui eux sont
bien stylés en CSS). Ça tombe bien, on va pouvoir exploiter ça pour être sûr⋅e⋅s de ne pas prendre
un lien en italiques : on va chercher seulement les `<a>` qui ne sont pas dans un `<i>`

```python
first_a = next(
    a
    for a in first_p.find_all("a")
    if not a.find_parents("i") and not is_between_parentheses(a, first_p)
)
first_a
```

On remet tout ça dans notre fonction

```python
def get_next_url(url):
    """Récupère la page à `url` et revoie l'addresse du premier lien du premier paragraphe"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    first_p = next(p for p in soup.body.find_all("p") if p.text and not p.text.isspace())
    first_link = next(
        a
        for a in first_p.find_all("a")
        if not a.find_parents("i") and not is_between_parentheses(a, first_p)
    )
    return urljoin(url, first_link["href"])
```

```python
next_url = "https://en.wikipedia.org/wiki/Algorithmic_bias"
for _ in range(16):
    print(next_url)
    next_url = get_next_url(next_url)
```

**argh**

## Fraught loops


Il y a une règle à laquelle Randall Munroe n'a pas pensé : les liens de référence, qui sont des
liens internes à la page (ils pointent vers une URL qui ne contient qu'une
[ancre](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_URL#anchor)) et
donc nous font tourner en rond. On va régler ça sauvagement en prenant le premier lien qui ne
commence pas par `#`.

```python
def get_next_url(url):
    """Récupère la page à `url` et revoie l'addresse du premier lien du premier paragraphe"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    first_p = next(p for p in soup.body.find_all("p") if p.text and not p.text.isspace())
    first_link = next(
        a
        for a in first_p.find_all("a")
        if not a["href"].startswith("#") and not a.find_parents("i") and not is_between_parentheses(a, first_p)
    )
    return urljoin(url, first_link["href"])
```

Note que ça ne nous protège pas des liens qui serait une redirection vers la même page, mais avec un
nom différent. Mais on se préoccupera de ça si on tombe dessus, comme c'est probablement assez rare

```python tags=["raises-exception"]
next_url = "https://en.wikipedia.org/wiki/Algorithmic_bias"
for _ in range(16):
    print(next_url)
    next_url = get_next_url(next_url)
```

Encore ?

## Le dernier problème

```python tags=["raises-exception"]
get_next_url("https://en.wikipedia.org/wiki/Logic")
```

Quel est le problème cette fois-ci ? Visiblement le premier paragraphe ne contient pas de lien 😱


C'est effectivement un truc auquel on avait pas pensé et qu'il faudra gérer, mais si on regarde bien
ce cas précis

```python
response = requests.get("https://en.wikipedia.org/wiki/Logic")
soup = BeautifulSoup(response.text, 'lxml')
first_p = next(p for p in soup.body.find_all("p") if p.text and not p.text.isspace())
first_p
```

C'est en fait un bout de la barre latérale, pas le *vrai* premier paragraphe


On va régler ça en cherchant nos liens dans les nœuds enfants *directs* (comme ça on esquive tous
les widgets) du cadre de contenu qui est visiblement toujours de la forme `<div
class="mw-parser-output" …>` et qu'on peut donc récupérer avec un sélecteur CSS.

```python
def get_next_url(url):
    """Récupère la page à `url` et revoie l'addresse du premier lien du premier paragraphe"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    
    # Un sélecteur CSS pour récupérer le contenu de la page
    page_content = soup.select(".mw-parser-output")[0]
    first_p = next(
        p
        for p in page_content.find_all("p", recursive=False)
        if p.text and not p.text.isspace()
    )
    first_link = next(
        a
        for a in first_p.find_all("a")
        if not a["href"].startswith("#")
        and not a.find_parents("i")
        and not is_between_parentheses(a, first_p)
    )
    return urljoin(url, first_link["href"])
get_next_url("https://en.wikipedia.org/wiki/Logic")
```

```python
next_url = "https://en.wikipedia.org/wiki/Algorithmic_bias"
for _ in range(29):
    print(next_url)
    next_url = get_next_url(next_url)
```

🥳


On va quand même prévoir l'avenir : il se pourrait qu'une page n'ait pas de lien dans le premier
paragraphe. On va donc plutôt itérer sur les paragraphes

```python
def get_next_url(url):
    """Récupère la page à `url` et revoie l'addresse du premier lien du premier paragraphe"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    page_content = soup.select(".mw-parser-output")[0]
    paragraphs = (
        p
        for p in page_content.find_all("p", recursive=False)
        if p.text and not p.text.isspace()
    )
    # On pourrait aussi faire une très grosse compréhension mais c'est déjà assez compliqué
    for p in paragraphs:
        # `None` en valeur par défaut si le générateur est vide
        first_link = next(
            (
                a
                for a in p.find_all("a")
                if not a["href"].startswith("#")
                and not a.find_parents("i")
                and not is_between_parentheses(a, p)
            ),
            None,
        )
        if first_link is not None:
            return urljoin(url, first_link["href"])

# Une page sans lien valide dans le premier paragraphe
get_next_url("https://en.wikipedia.org/wiki/Creativity")
```

## Le poète des cercles disparus


Il ne reste plus qu'à écrire une fonction qui

- Prend la page de départ en entrée
- Suis les liens jusqu'à
  - Tomber sur *Philosophy*
  - Ou sur une page déjà visitée (pour éviter de tourner en rond)
- Renvoie le nombre de pages visitées

On *pourrait* le faire en récursif, mais ça rend la détection des cycles et le compte des sauts
pénibles alors on va simplement faire une boucle.

```python
import sys

# On va modifier la fonction `get_next_url` parce qu'on va se servir de la soupe pour d'autre choses
# et on veut éviter de parser plusieurs fois la même page
def get_first_url(soup):
    """Renvoie l'addresse du premier lien du premier paragraphe dans une soupe"""
    page_content = soup.select(".mw-parser-output")[0]
    paragraphs = (
        p
        for p in page_content.find_all("p", recursive=False)
        if p.text and not p.text.isspace()
    )
    for p in paragraphs:
        first_link = next(
            (
                a
                for a in p.find_all("a")
                if not a["href"].startswith("#")
                and not a.find_parents("i")
                and not is_between_parentheses(a, p)
            ),
            None,
        )
        if first_link is not None:
            return first_link["href"]


def search_for(start_url, target_title="Philosophy"):
    next_url = start_url
    # Les initialisations bizarres c'est parce qu'on va devoir faire au moins un tour de boucle pour
    # vérifier le titre de la page de départ (utile par exemple si on est dans une redirection)
    n_hops = -1
    title = None
    # Ça devrait être marginalement plus rapide avec un set pour qui insertion et test d'inclusion
    # sont en moyenne O(1) qu'avec une liste qui est aussi en O(1) (mais plus rapide en moyenne)
    # pour l'insertion mais O(n) pour le test d'inclusion. Voir
    # <https://wiki.python.org/moin/TimeComplexity>
    visited = set()
    while title != target_title:
        n_hops += 1
        response = requests.get(next_url)
        soup = BeautifulSoup(response.text, "lxml")
        # Les titres sont de la forme  "{titre de page} - Wikipedia"
        title = soup.title.string.split(" - ")[0]
        # On va afficher le trajet, ça nous distraira. Pour des applications sérieuses, on utilisera
        # une bibli de log comm [loguru](https://loguru.readthedocs.io)
        print(title, file=sys.stderr)
        # On a trouvé un cycle
        if title in visited:
            # On sait que c'est pas `target_title` sinon on serait sorti de la boucle avant,
            # puisqu'on l'a déjà visité. On peut donc être certain⋅e⋅s qu'on atteindra jamais la
            # cible. Plutôt que de faire des fantaisies à renvoyer `math.inf` ou je ne sais quoi, on
            # va sobrement renvoyer `-1`. On pourrait aussi lever une exception.
            return -1
        next_url = urljoin(next_url, get_first_url(soup))
    return n_hops
```

```python
search_for("https://en.wikipedia.org/wiki/Algorithmic_bias")
```

Et on en fait [un script](wikipedia_soup.py)

```python
%run wikipedia_soup "https://en.wikipedia.org/wiki/Python_(programming_language)"
```

Regarde, on peut même partir d'une page au hasard grâce à <https://en.wikipedia.org/wiki/Special:Random>

```python
search_for("https://en.wikipedia.org/wiki/Special:Random")
```

## Des graphes des graphes des graphes

Si on est très motivé⋅e⋅s, on va essayer de visualiser la structure que ça donne à Wikipédia. Pour
ça on peut se servir de [ipycytoscape](https://github.com/cytoscape/ipycytoscape)

```python
%pip install ipycytoscape
```

```python
import ipycytoscape
import ipywidgets as widgets
import networkx as nx
```

Il s'agit d'un paquet pour visualiser interactivement des graphes dans des notebooks. Par exemple
avec [NetworkX](networkx.org) (qu'on peut utiliser en standalone pour des scripts)

```python
G = nx.complete_graph(5)
directed = ipycytoscape.CytoscapeWidget()
directed.graph.add_graph_from_networkx(G, directed=True)
directed
```

## Des refs ?

- [La page de Wikipedia sur ce sujet](https://en.wikipedia.org/wiki/Wikipedia:Getting_to_Philosophy)
- Un article qui traite d'une généralisation du problème :

  - Lamprecht, Daniel, Dimitar Dimitrov, Denis Helic, and Markus Strohmaier. [‘Evaluating and
    Improving Navigability of Wikipedia: A Comparative Study of Eight Language
    Editions’](https://dl.acm.org/doi/10.1145/2957792.2957813?cid=81100338950). In Proceedings of
    the 12th International Symposium on Open Collaboration, 1–10. OpenSym ’16. New York, NY, USA:
    Association for Computing Machinery, 2016. <https://doi.org/10.1145/2957792.2957813>.

