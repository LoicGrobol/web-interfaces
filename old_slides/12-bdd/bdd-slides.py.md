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

```python

```

<!-- #region slideshow={"slide_type": "slide"} -->
Cours 12 : FastAPI et les bases de données relationnelles
=========================================================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

<!-- #endregion -->


```python
from IPython.display import display
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Bases de données

Les bases de données en 30s pour les Pythonista pressé⋅e⋅s :

- Une **entrée** dans une base de données, c'est comme un tuple nommé : c'est une série ordonnée de
  valeurs, chacune associée à une clé.
  
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
- Une **table**, c'est une liste d'entrées qui ont toutes les mêmes clés. On pense souvent aux
  entrées comme aux lignes (*row*) d'un tableau et aux clés comme des colonnes.
  - Une des clés sert d'identifiant : on l'appelle la **clé primaire** et la valeur associée doit
     être unique pour chacune des entrées de la table.
  - souvent, une des colonnes a comme valeurs des clés primaires d'entrées d'une autre
    table
    - Ça permet de créer des liens entre tables.
    - On dit dans ce cas que cette colonne est une **clé étrangère**.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
- Une **base de données**, c'est un ensemble de tables.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
On peut raffiner beaucoup ce modèle pour des usages avancés et il existe d'autres façons d'envisager
les bases de données, mais en ce qui nous concerne ça suffira.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Les bases de données sont un concept crucial en informatique, aussi bien en théorie qu'en pratique
et elles sont très vite nécessaire dès qu'on gère des grandes quantités d'informations structurées.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Il y a plein de façons d'implémenter une base de données : on peut tout à fait envisager une base de
données implémentée en Python comme une liste de listes de tuples nommés et sauvegardée dans un
fichier JSON. En pratique, on fait rarement ça parce que

- Lire un fichier à chaque recherche, c'est long.
- Réécrire un fichier à chaque modification, c'est très long.
- Avoir plusieurs processus qui accèdent en même temps à un fichier c'est compliqué.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Le modèle qu'on suit habituellement est plutôt un modèle client-serveur : un programme (le
gestionnaire) gère la base de données et les autres programmes y accèdent en passant des messages au
gestionnaire, souvent dans un langage adapté comme SQL (_**S**tructured ~~**Q**ueering~~ **Q**uery
**L**anguage_).
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
```sql
create table recettes (id int not null primary key, nom varchar, texte text);
insert into recettes values (0, 'Tartelettes amandines', 'Battez pour qu''ils soient mousseux quelques œufs');
select * from recettes where nom='Tartelettes amandines';
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
<small>Notez la façon extrêmement maudite de déspécialiser le simple quote</small>
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Les détails (sous quelle forme est stockée la base, comment y sont faites les requêtes…) sont
internes au gestionnaire. Toujours la séparation des préoccupations.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## SQLite

/ˌɛsˌkjuːˌɛlˈaɪt/ en anglais, /ˈsiːkwəˌlaɪt/ pour la frime, pour moi le plus souvent /ɛskylajt/

SQLite est une bibliothèque minimaliste de bases de données, à laquelle on peut accéder en Python
depuis le module [`sqlite3`](https://docs.python.org/3/library/sqlite3.html) de la bibliothèque
standard. Elle a deux particularités qui nous arrangent bien :

- Elle ne nécessite pas de gestionnaire séparé : votre script peut accéder à la base sans passer par
  un autre processus.
- Les bases sont stockées dans des fichiers uniques.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
C'est très avantageux pour nous : on a pas à s'imposer l'installation et la configuration d'un
système de gestion de bases de données, la création d'utilisateurs avec des droits et tout le
*boilerplate* qui est utile pour des grosses applications, mais un sacré frein pour nous.

Le revers de la médaille, c'est que si l'application devient plus complexe, qu'on a besoin de plus
de fonctions, de gestion plus fine, ça ne suffira plus. **Cependant** il sera toujours temps de
migrer plus tard si besoin : « *premature optimisation is the root of all evil* ».
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
import sqlite3
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Comment on ouvre une base de données en SQLite ? On a dit que c'était juste un fichier, et bien il
suffit de donner son chemin
<!-- #endregion -->

```python
con = sqlite3.connect("db.sqlite3")
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Ça crée le fichier s'il n'existe pas déjà, lit la base de donnée qui est dedans et vous y donne
accès. On peut aussi passer `":memory:"` à la place d'un chemin, ce qui créé la base en RAM plutôt
que comme un fichier.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
On fait ce qu'on a à y faire, puis on ferme la connexion.
<!-- #endregion -->

```python
con.close() 
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Astuce : on peut utiliser [`contextlib.closing`](https://docs.python.org/3/library/contextlib.html#contextlib.closing) pour le faire automatiquement et proprement
<!-- #endregion -->

```python
from contextlib import closing
with closing(sqlite3.connect("db.sqlite3")) as con:
    pass  # Faire des trucs ici
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Ok, super, on a ouvert et fermé un fichier, mais comment on accède à la base ?
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
Avec un [curseur](https://docs.python.org/3/library/sqlite3.html#cursor-objects)
<!-- #endregion -->

```python
with closing(sqlite3.connect("db.sqlite3")) as con:
    cur = con.cursor()
    cur.execute("create table if not exists recettes (id int not null primary key, nom varchar, texte text)")
    cur.execute("insert into recettes values (0, 'Tartelettes amandines', 'Battez pour qu''ils soient mousseux quelques œufs')")
    con.commit()
    cur.execute("select * from recettes where nom='Tartelettes amandines';")
    print(cur.fetchall())
    cur.close()
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Quelques trucs à noter

- On exécute des commandes en SQL avec la méthode `execute` d'un curseur. On peut aussi exécuter
  tout un script avec `executescript` ou — mieux, voir plus bas — `executemany`
- Une fois qu'elles sont exécutées, il faut les valider en utilisant la méthode `commit` de la
  connexion. Tant qu'on ne l'a pas fait, rien ne se passe.
- Pour récupérer les résultats d'une requête on peut utilise les méthodes `fetchone`, `fetchall` ou
  `fetchmany` du curseur. Comme d'hab, la
  [doc](https://docs.python.org/3/library/sqlite3.html#cursor-objects) est votre amie.
- On ferme les curseurs avec leur méthode `close`
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
On peut récupérer un résumé de la table sous la forme des commandes SQL qui permettent de la recopier à l'identique avec `iterdump`
<!-- #endregion -->

```python
with closing(sqlite3.connect("db.sqlite3")) as con:
    for l in con.iterdump():
        print(l)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Attention quand vous construisez des instructions SQL à partir d'entrées que vous ne maîtrisez pas
<!-- #endregion -->

```python
with closing(sqlite3.connect("db.sqlite3")) as con:
    cur = con.cursor()
    cur.executescript("""
    insert into recettes values (2, 'Tiramisu', 'Aucune idée mais c''est délicieux');
    insert into recettes values (3, 'Seitan bolognaise', 'Commencer par faire du seitan');
    """
    )
    con.commit()
    cur.execute("select * from recettes")
    print(cur.fetchall())
    cur.close()
```

```python
def read_recette(name):
    with closing(sqlite3.connect("db.sqlite3")) as con:
        cur = con.cursor()
        cur.execute(f"select * from recettes where nom='{name}'")
        res = cur.fetchall()
        cur.close()
    return res

read_recette("Tiramisu")
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Pas de problème jusque là, mais si un individu malveillant passe un nom qui contient du code :
<!-- #endregion -->

```python
read_recette("Tiramisu' or nom <> 'Tiramisu")
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Ça dumpe toute la table ! Si vous avez eu la mauvaise idée de faire ça dans un `executescript` c'est
pire, vous risquez de rencontrer Bobby Tables

[![](https://imgs.xkcd.com/comics/exploits_of_a_mom.png)](https://xkcd.com/327)
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Pour éviter ça : on utilise des requêtes paramétrées qui seront assainies pour nous
<!-- #endregion -->

```python
def read_recette(name):
    with closing(sqlite3.connect("db.sqlite3")) as con:
        cur = con.cursor()
        cur.execute("select * from recettes where nom=:lenom", {"lenom": name})
        res = cur.fetchall()
        cur.close()
    return res

display(read_recette("Tiramisu"))
display(read_recette("Tiramisu' or nom <> 'Tiramisu"))
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Avec ça (et un manuel de SQL sous la main) vous avez l'essentiel de ce qu'il faut pour gérer des
bases de données en SQLite. On l'a dit, c'est minimaliste.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Une dernière astuce ? On peut récupérer des mappings plutôt que des tuples avec `fetch…` :
<!-- #endregion -->

```python
def read_recette(name):
    with closing(sqlite3.connect("db.sqlite3")) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from recettes where nom=:lenom", {"lenom": name})
        res = cur.fetchall()
        cur.close()
    return res

recettes = read_recette("Tiramisu")
[r["texte"] for r in recettes]
```

<!-- #region slideshow={"slide_type": "slide"} -->
## 🌲 Exo 🌲

Écrire un script qui construit une base de données en SQLite qui contient une table à trois colonnes
qui représente un treebank Universal Dependencies. La première colonne qui servira de clé primaire
contiendra pour chaque arbre son attribut `sent_id`, la deuxième contiendra son attribut `text`,
enfin la dernière contiendra l'arbre syntaxique qu format CoNLL-U. Remplissez cette base avec le
contenu d'un treebank UD de votre choix. Vous pouvez vous aider de
[`conllu`](https://github.com/EmilStenstrom/conllu) pour faire le boulot de parser le fichier.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Utiliser une base de données dans FastAPI

C'est assez courant d'avoir besoin de bases de données pour des applications complexes. Les cas
typiques sont

- Une base qui rassemble des données qu'on compte présenter aux utilisateurices (par exemple avec la
  base de l'exo précédent on peut vouloir leur permettre de faire des recherches dans un treebank)
- Une base à usage interne comme une base d'utilisateurices qui stocke leur nom, leur avatar, leurs
  paramètres, des infos de connexion (comme un hash du mot de passe)…
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Ce n'est pas très compliqué, voyons ensemble un exemple :
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
# %load apis/simple.py
from typing import List
import sqlite3

from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()


def get_db():
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    try:
        yield cur
        con.commit()
    finally:
        cur.close()
        con.close()


# Database setup
con = sqlite3.connect("db.sqlite3")
cur = con.cursor()
cur.execute(
    "create table if not exists trees (tree_id VARCHAR NOT NULL PRIMARY KEY, text TEXT)"
)
cur.close()
con.close()


class Tree(BaseModel):
    tree_id: str
    text: str


# Methods for interacting with the database
def get_tree(cur: sqlite3.Cursor, tree_id: str):
    cur.execute("select * from trees where tree_id=:tree_id", {"tree_id": tree_id})
    db_tree_id, db_text = cur.fetchone()
    return {"tree_id": db_tree_id, "text": db_text}


def get_trees(cur: sqlite3.Cursor):
    cur.execute("select * from trees")
    return [
        {"tree_id": db_tree_id, "text": db_text}
        for db_tree_id, db_text in cur.fetchall()
    ]


def create_tree(cur: sqlite3.Cursor, tree: Tree):
    cur.execute(
        "insert into trees values (:tree_id, :text)",
        {"tree_id": tree.tree_id, "text": tree.text},
    )
    return tree


@app.post("/trees/", response_model=Tree)
def create_trees_view(tree: Tree, db: sqlite3.Cursor = Depends(get_db)):
    db_tree = create_tree(db, tree)
    return db_tree


@app.get("/trees/", response_model=List[Tree])
def get_trees_view(db: sqlite3.Cursor = Depends(get_db)):
    return get_trees(db)


@app.get("/tree/{tree_id}")
def get_tree_view(tree_id: str, db: sqlite3.Cursor = Depends(get_db)):
    return get_tree(db, tree_id)

```

<!-- #region slideshow={"slide_type": "subslide"} -->
Ça marche exactement comme les API qu'on a déjà réalisé, simplement les opérations font appel à
`sqlite3` pour interagir avec une base de données.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Le seul truc nouveau ici (mais dont on aurait pû se passer) c'est l'utilisation de `Depends` et
`get_db` : il s'agit d'une [injection de
dépendance](https://fastapi.tiangolo.com/tutorial/dependencies)
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
Quand un paramètre dans un point d'accès a comme valeur par défaut `Depends(get_db)`, il n'est pas récupéré à partir de la requête mais en récupérant ce qui est renvoyé par le générateur `get_db` avec `yield`.

Une fois la fonction correspondant au point d'accès terminée, FastAPI reprends l'exécution de `get_db` pour faire un `commit`, puis fermer le curseur et la base.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
Ces dernières opérations sont placées dans la clause `finally` d'un bloc `try:`, ce qui assure
qu'elles seront exécutées même si la méthode d'API ou le `commit` échouent.
<!-- #endregion -->

Pour une utilisation plus agréable sans écrire de requêtes SQL à la main, on peut utiliser
[SQLAlchemy](https://docs.sqlalchemy.org) qui s'intègre bien avec FastAPI

```python
# %load apis/full_treebank.py
from typing import List
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Column, String, Text

app = FastAPI()

# SqlAlchemy Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite3"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Tree(BaseModel):
    tree_id: str
    text: str

    class Config:
        orm_mode = True


class DBTree(Base):
    __tablename__ = "trees"

    tree_id = Column(String, primary_key=True, index=True)
    text = Column(Text)


Base.metadata.create_all(bind=engine)


# Methods for interacting with the database
def get_tree(db: Session, tree_id: str):
    return db.query(
        DBTree
    ).where(
        DBTree.tree_id == tree_id
    ).first()


def get_trees(db: Session):
    return db.query(DBTree).all()


def create_tree(db: Session, tree: Tree):
    db_tree = DBTree(**tree.dict())
    db.add(db_tree)
    db.commit()
    db.refresh(db_tree)

    return db_tree


@app.post("/trees/", response_model=Tree)
def create_trees_view(tree: Tree, db: Session = Depends(get_db)):
    db_tree = create_tree(db, tree)
    return db_tree


@app.get("/trees/", response_model=List[Tree])
def get_trees_view(db: Session = Depends(get_db)):
    return get_trees(db)


@app.get("/tree/{tree_id}")
def get_tree_view(tree_id: str, db: Session = Depends(get_db)):
    return get_tree(db, tree_id)


@app.post("/trees/")
async def create_tree_view(tree: Tree):
    return tree

```

C'est essentiellement la même chose, en plus agréable à écrire mais aussi en plus magique. À vous de
voir ce que vous préférez, FastAPI a [un
tutoriel](https://fastapi.tiangolo.com/tutorial/sql-databases) sur l'utilisation de SQLAlchemy pour
un gestionnaire d'utilisateurices basique.


Ça vaut aussi le coup de lire un jour [le tutoriel de
SQLAlchemy](https://docs.sqlalchemy.org/en/14/tutorial) qui est plus ou moins la bibliothèque
standard pour travailler avec des bases de données relationnelle en Python. C'est un peu touffu mais
ça se fait en prenant son temps et vous vous remercierez plus tard (et qui ne voudrait pas être un⋅e
alchimiste ?).

<small>Bien sûr il n'y a pas que les BDD relationnelles dans la vie et vous aurez probablement à
travailler avec d'autres trucs comme MongoDB mais ceci est une autre histoire</small>


Pour la gestion d'utilisateurices en particulier : sur un prototype ça peut se faire à la main, mais
très très vite l'idéal est de passer à une bibliothèque comme [FastAPI
Users](https://fastapi-users.github.io/fastapi-users/) qui gère pour vous les opérations standard
comme la gestion de mots de passe tout en vous laissant personnaliser ce dont vous avez besoin. 
