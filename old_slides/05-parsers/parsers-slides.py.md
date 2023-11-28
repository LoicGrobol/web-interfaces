---
jupyter:
  jupytext:
    formats: ipynb,md
    split_at_heading: true
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.2
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- LTeX: language=fr -->

<!-- #region slideshow={"slide_type": "slide"} -->
Cours 5 : Parser des documents balisés avec `lxml` et BeautifulSoup
==================================================================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

<!-- #endregion -->

```python
from IPython.display import display
```

## Documents balisés

## `lxml` ? Beautiful Soup ?

`lxml`. Beautiful Soup.

[`lxml`](http://lxml.de/) est un parseur de documents balisés, fonctionnant via un *binding* de la
bibliothèque [`libxml2`](http://xmlsoft.org/). Il est conçu pour être rapide (*très* rapide) et très
près du standard. [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) est une
*interface* d'accès pour HTML (et XML) conçu pour être la plus souple et facile d'utilisation
possible (un peu la même philosophie que `requests`) et pour rendre facile le travail sur des
documents potentiellement mal formés.

Installons ces modules, soit dans votre terminal avec `pip`, soit en exécutant la cellule de code
suivante. Comme d'habitude, il est vivement recommandé de travailler pour ce cours dans un
environnement virtuel et si vous avez installé le [requirements.txt](../../requirements.txt) de ce
cours, ces modules sont déjà installés. Nous aurons également besoin de `requests` [que nous avons
déjà utilisé](../04-requests/requests-slides.py.md) et plus anecdotiquement de `matplotlib`.


```python
%pip install -U beautifulsoup4 lxml matplotlib requests
```

```python
from bs4 import BeautifulSoup
import lxml
import requests
```

## Parser du HTML

[On ne parse pas du HTML avec de regex](https://stackoverflow.com/a/1732454)

(sauf quand on le fait quand même)

(mais pas ici)

(non mais)

Beautiful Soup permet de parser simplement du contenu HTML. Même si le contenu est mal formé, le
module reconstitue un arbre et offre des fonctions faciles à utiliser pour le parcourir ou y
rechercher des éléments.

Beautiful Soup n'est pas un parseur, mais *utilise* des parseurs.

Nous travaillerons directement avec du contenu en ligne. Fini les exercices bidons, cette fois nous
allons nous confronter à une question essentielle : combien d'accordages *open tuning* Neil Young
utilise et comment sont-ils répartis dans son œuvre ?  
On trouve les infos sur les chansons de Neil Young et les accordages sur le fabuleux site
[songx.se](http://songx.se/index.php) (le site ayant changé d'interface, nous utiliserons une
archive de [Wayback Machine](http://web.archive.org/))


Avec `requests` pour récupérer les données, nous allons pouvoir instancier un objet Beautiful Soup
sans trop d'efforts

```python
import requests
from bs4 import BeautifulSoup

url = "http://web.archive.org/web/20180430090903/http://songx.se/index.php" # le lien vers le site
html = requests.get(url) # on récupère le contenu
soup = BeautifulSoup(html.text, 'lxml') # on crée un objet pour traiter la page
```

Voilà nous avons maintenant un objet `soup` de classe [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#beautifulsoup).

La [doc](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) est très claire.

Chercher un élément avec le tag `title`

```python
e = soup.title
e
```

Récupérer son tag

```python
e.name
```

Récupérer son contenu textuel

```python
e.string
```

<!-- #region -->
Les informations qui nous intéressent sont contenues dans des éléments comme celui-ci (formaté pour
une meilleure lisibilité) :

```html
<div class="songrow">
    <a href="?song=505">Clementine</a>
    <small>(cover)</small>
    <div style="float:right;">EADGBE</div>
</div>
```

Où on trouve le nom de la chanson (`Clementine`) et l'accord utilisé (`EADGBE`)
<!-- #endregion -->

### 🎶 Exo 1 🎶

1\. Affichez les titres et les tunings des 10 premières chansons en utilisant la méthode
[`find_all`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all). La méthode renvoie un
itérable.

```python
for item in soup.find_all([...]):
    print(item.[...], item.[...])
```

2\. Créez un `dict` appelé `tunings` qui classe les chansons par tuning (autrement dit qui associe à
un tuning la liste des morceaux qui l'utilisent). (On peut utiliser plus sympa qu'un bête `dict`).
Lisez bien [la doc de `find_all`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all).

```python
from typing import Dict, List
tunings: Dict[str, List[str]] = dict()
for item in soup.find_all([...]):
    song_title = item.[...]
    tuning = item.[...]
    [...]
```

(`typing` c'est quoi ? Qu'est-ce que ça veut dire `Dict[str, List[str]]` ? On en reparlera si on a le
temps mais vous pouvez prendre de l'avance [sur Real
Python](https://realpython.com/python-type-checking/))

3\. 'Harvest Moon' utilise l'accordage DADGBE, y en a-t'il d'autres ?

```python
print([...])
```

4\. Affichez les accordages et le nombre de chansons pour chaque accordage, le tout trié par nombre de
chansons décroissant. Pour cela, cous utiliserez la méthode `sorted` ainsi que l'argument mot-clé
`key` (des exemples [ici](https://wiki.python.org/moin/HowTo/Sorting#Key_Functions)) :

```python
for tuning in sorted(tunings.keys(), key=[...]):
    print([...])
```

Allez hop un histogramme

```python
%matplotlib inline
import matplotlib.pyplot as plt
values = [len(tunings[x]) for x in tunings]
values
plt.bar(range(0, len(values)), values)
plt.xticks(range(0, len(values)), tunings.keys(), rotation=17)

plt.show()
```

5\. Une chanson a un tuning un peu particulier comparé aux autres (indice, c'est une question de
taille). Trouvez le tuning qui est différent des autres et donnez la chanson qui lui correspond.
_Attention_, "b" signifie "bémol", il ne s'agit pas d'une note pour l'accordage (contrairement à A,
B, C, D, E, F et G) !


## Parser du XML

Nous allons travailler sur un fichier au format [TEI](http://www.tei-c.org/) extrait du corpus
[*Corpus 14*](https://hdl.handle.net/11403/corpus14/v1).

Le fichier se nomme [`josephine-1-150119.xml`](data/josephine-1-150119.xml). Il s'agit d'une
lettre d'une femme de soldat à son époux. Les chemins du notebook devraient fonctionner sur Binder,
pour bosser en local, vous pouvez le récupérer sur
[GitHub](https://raw.githubusercontent.com/LoicGrobol/web-interfaces/main/data/josephine-1-150119.xml)

Nous allons extraire du fichier TEI les informations suivantes :

- titre (`/TEI/teiHeader/fileDesc/titleStmt/title`)
- source (`/TEI/teiHeader/fileDesc/sourceDesc/p`)
- contenu de la lettre (`/TEI/text/body`)

Vous pouvez trouver des indications sur les éléments de la TEI
[ici](http://www.tei-c.org/release/doc/tei-p5-doc/fr/html/) (ça pourra être utile pour les
questions)

### Avec lxml

Pourquoi `lxml` et pas `xml.etree.ElementTree` ? Parce que : [1](http://lxml.de/intro.html) et
surtout [2](http://lxml.de/performance.html).

La bonne nouvelle, c'est que votre code sera aussi compatible avec `xml.etree.ElementTree` ou
`xml.etree.cElementTree` parce que xml utilise l'API ElementTree. Sauf pour la méthode `xpath` qui
est propre à `libxml`.

```python
from lxml import etree
tree = etree.parse('data/josephine-1-150119.xml')
root = tree.getroot()

# Parcours des enfants de la racine (commentaires et éléments)
for child in root:
    print(child.tag)
```

### Avec des requêtes `ElementPath`

Le fichier utilise l'[espace de nom](https://fr.wikipedia.org/wiki/Espace_de_noms_XML) TEI : `<TEI
xmlns="http://www.tei-c.org/ns/1.0">`, nous devrons l'indiquer dans nos instructions de recherche.

Nous pouvons récupérer un élément particulier qui correspond à un chemin : par exemple, pour
récupérer le *header* TEI dont le chemin est `/TEI/teiHeader`

la méthode `find` renvoie le premier élément qui correspond au chemin argument (`ElementPath` et non
`xpath`)

```python
header = root.find("./tei:teiHeader", namespaces={'tei':"http://www.tei-c.org/ns/1.0"})
header
```

### 🧭 Exo 🧭

1\. Récupérez le titre et affichez son tag XML ainsi que son contenu textuel (`/TEI/teiHeader/fileDesc/titleStmt/title`)

```python
title = root.find("[...]", namespaces={'tei':"http://www.tei-c.org/ns/1.0"})
print("Tag : {}".format(title.tag))
print("Texte : {}".format(title.text))
```

2\. Idem pour la source (élément `sourceDesc`) :

```python
source = root.find("[...]", namespaces={'tei':"http://www.tei-c.org/ns/1.0"})
print("Tag : {}".format(source.tag))
print("Texte : {}".format(source.text))
```

### Avec des requêtes xpath

`lxml` a aussi une méthode [xpath](https://lxml.de/xpathxslt.html) qui permet d'utiliser directement
des [expressions xpath](https://www.w3schools.com/xml/xpath_syntax.asp) (sans oublier les espaces de
noms pour notre fichier) :

```python
source = root.xpath(
    "/tei:TEI/tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:p",
    namespaces={'tei':'http://www.tei-c.org/ns/1.0'},
)
print(f"xpath retourne un objet de type {type(source)}")
print(source[0].text)
```

Ou comme ceci

```python
source = root.xpath(
    "/tei:TEI/tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:p/text()",
    namespaces={'tei':'http://www.tei-c.org/ns/1.0'},
)
print(source[0])
```

Pour le contenu il faut ruser. La difficulté ici tient à l'utilisation d'élements `<lb/>` de type
[milestones](http://www.tei-c.org/release/doc/tei-p5-doc/fr/html/CO.html#CORS5) pour noter les
retours à la ligne :

```xml
<p>
je reponse a ton aimableux lettres<lb/>
que nous a fait plaisir en naprenas<lb/>
que tu et enbonne santes car il<lb/>
anais de maime pour nous<lb/>
</p>
```

### 🥲 Exo 🥲

1\. Récupérez dans un premier temps l'ensemble des balises `<p>` en utilisant la méthode
[findall](http://effbot.org/zone/element.htm#searching-for-subelements). la méthode `findall`
renvoie une liste avec tous les éléments correspondant au chemin argument.

```python
body = root.findall("./[...]", namespaces={'tei':"http://www.tei-c.org/ns/1.0"})
for elem in body: # tout le texte ne s'affichera pas, c'est normal !
    print(elem.text)
```

Ici on ne récupère que les nœuds `text` précédant les éléments `<lb/>`.

2\. Utilisez la fonction `xpath` pour récupérer tous les nœuds text du corps de la lettre. Vous
intégrerez dans votre requête la fonction `text` (vue un peu plus haut) dans votre chemin xpath
(vous pouvez _aussi_ fouiller [par ici](https://lxml.de/xpathxslt.html) pour avoir de la
documentation supplémentaire).

```python
body = root.xpath("[...]", namespaces={'tei':"http://www.tei-c.org/ns/1.0"})
for text in body:
    print(text, end="")
```

3\. Écrivez une requête xpath pour récupérer tous les éléments raturés de la lettre de Joséphine.

## Avec DOM

L'API `ElementTree` est propre à Python, `DOM` ([le site officiel](https://www.w3.org/DOM/) et [des
informations en français](https://developer.mozilla.org/fr/docs/Web/API/Document_Object_Model)) est
une API indépendante d'un langage de programmation. Il existe des implémentations `DOM` dans la
plupart des langages de programmation modernes.  

```python
from xml.dom import minidom
dom = minidom.parse("data/josephine-1-150119.xml")
dom
```

```python
# un seul élément 'title' dans le document
title = dom.getElementsByTagNameNS("http://www.tei-c.org/ns/1.0", 'title')[0]
title
```

`title` est un objet `Element`, pour accéder au contenu textuel il faut récupérer le nœud texte

```python
print(title) 
print(title.lastChild.nodeName)
print(title.lastChild.nodeValue)
```

Idem pour la source, sauf qu'on ne peut pas se permettre de rechercher tous les éléments `p`.  
Il faut trouver l'élément `p` fils de `sourceDesc`

```python
sourceDesc = dom.getElementsByTagNameNS("http://www.tei-c.org/ns/1.0", 'sourceDesc')[0]
for node in sourceDesc.childNodes:
    if node.localName == "p":
        print(node.lastChild.nodeValue)
```

Et maintenant le contenu et ses éléments milestones

### 😌 Exo 😌

Pour garder la forme, vous réécrirez les boucles `for` suivies de `if` en listes en intension.

```python
body = dom.getElementsByTagNameNS("http://www.tei-c.org/ns/1.0", 'body')[0]
for node in body.childNodes:
    if node.localName in ("p", "opener"):
        for in_node in node.childNodes:
            if in_node.nodeName == "#text":
                print(in_node.nodeValue, end="")
```

## Avec lxml et Beautiful Soup

```python
from bs4 import BeautifulSoup

with open("data/josephine-1-150119.xml") as fp:
    soup = BeautifulSoup(fp, 'lxml')
```

```python
soup.title.text
```

```python
soup.sourcedesc.p.text
```

Pour le contenu de la lettre il y a la merveilleuse fonction `get_text()`

```python
soup.get_text?
```

```python
text = soup.find("text")
print(text.getText())
```

`lxml` est rapide, Beautiful Soup simple à utiliser. Le combo diablement efficace.

Il y a un autre module super pour le web que nous ne verrons pas dans cette séance mais que je me
dois de vous indiquer : [Selenium](https://selenium-python.readthedocs.io/) Selenium va vous
permettre d'automatiser des actions sur un navigateur. Je vous conseille d'essayer, c'est assez
plaisant de voir votre navigateur piloté par un script. C'est aussi génial pour tester
automatiquement les interfaces web que vous développez

## 🤔 Exo d'application 🤔

> Wikipedia trivia: if you take any article, click on the first link in the article text not in
> parentheses or italics, **and then repeat**, you will eventually end up at "Philosophy". ([xkcd
> #903](https://xkcd.com/903/))

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
