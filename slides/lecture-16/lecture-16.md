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
Cours 16 : FastAPI et les bases de données relationnelles
=========================================================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

2021-11-17
<!-- #endregion -->


```python
from IPython.display import display
```

## Bases de données

Les bases de données en 30s pour les Pythonista pressé⋅e⋅s :

- Une **entrée** dans une base de données, c'est comme un tuple nommé : c'est une série ordonnée de
  valeurs, chacune associée à une clé.
- Une **table**, c'est une liste d'entrées qui ont toutes les mêmes clés. On pense souvent aux
  entrées comme aux lignes (*row*) d'un tableau et aux clés comme des colonnes.
  - Une des clés sert d'identifiant : on l'appelle la **clé primaire** et la valeur associée doit
     être unique pour chacune des entrées de la table.
  - Il arrive souvent qu'une des colonnes ait comme valeurs des clés primaires d'entrées d'une autre
    table, ça permet de créer des liens entre tables. On dit dans ce cas que cette colonne est une
    **clé étrangère**.
- Une **base de données**, c'est un ensemble de tables.

On peut raffiner beaucoup ce modèle pour des usages avancés et il existe d'autres façons d'envisager
les bases de données, mais en ce qui nous concerne ça suffira.

Les bases de données sont un concept crucial en informatique, aussi bien en théorie qu'en pratique
et elles sont très vite nécessaire dès qu'on gère des grandes quantités d'informations structurées.

Il y a plein de façons d'implémenter une base de données : on peut tout à fait envisager une base de
données implémentée en Python comme une liste de listes de tuples nommés et sauvegardée dans un
fichier JSON. En pratique, on fait rarement ça parce que

- Lire un fichier à chaque recherche, c'est long.
- Réécrire un fichier à chaque modification, c'est très long.
- Avoir plusieurs processus qui accèdent en même temps à un fichier c'est compliqué.

Le modèle qu'on suit habituellement est plutôt un modèle client-serveur : un programme (le
gestionnaire) gère la base de données et les autres programmes y accèdent en passant des messages au
gestionnaire, souvent dans un langage adapté comme SQL (_**S**tructured ~~**Q**ueering~~ **Q**uery
**L**anguage_).

<!-- #region -->
```sql
create table recettes (id int not null primary key, nom varchar, texte text);
insert into recettes values (0, 'Tartelettes amandines', 'Battez pour qu''ils soient mousseux quelques œufs');
select * from recettes where nom='Tartelettes amandines';
```
<!-- #endregion -->

<small>Notez la façon extrêmement maudite de déspécialiser le simple quote</small>


Les détails (sous quelle forme est stockée la base, comment y sont faites les requêtes…) sont
internes au gestionnaire. Toujours la séparation des préoccupations.

## SQLite

/ˌɛsˌkjuːˌɛlˈaɪt/ en anglais, /ˈsiːkwəˌlaɪt/ pour la frime, pour moi le plus souvent /ɛskylajt/

SQLite est une bibliothèque minimaliste de bases de données, à laquelle on peut accéder en Python
depuis le module [`sqlite3`](https://docs.python.org/3/library/sqlite3.html) de la bibliothèque
standard. Elle a deux particularités qui nous arrangent bien :

- Elle ne nécessite pas de gestionnaire séparé : votre script peut accéder à la base sans passer par
  un autre processus.
- Les bases sont stockées dans des fichiers uniques.

C'est très avantageux pour nous : on a pas à s'imposer l'installation et la configuration d'un
système de gestion de bases de données, la création d'utilisateurs avec des droits et tout le
*boilerplate* qui est utile pour des grosses applications, mais un sacré frein pour nous.

Le revers de la médaille, c'est que si l'application devient plus complexe, qu'on a besoin de plus
de fonctions, de gestion plus fine, ça ne suffira plus. **Cependant** il sera toujours temps de
migrer plus tard si besoin : « *premature optimisation is the root of all evil* ».

```python
import sqlite3
```

Comment on une base de données en SQLite ? On a dit que c'était juste un fichier, et bien il suffit de donner son chemin

```python
con = sqlite3.connect("db.sqlite3")
```

Ça créé le fichier s'il n'existe pas déjà, lit la base de donnée qui est dedans et vous y donne accès. On peut aussi passer `":memory:` à la place d'un chemin, ce qui créé la base en RAM plutôt que comme un fichier.


On fait ce qu'on a à y faire, puis on ferme la connexion.

```python
con.close()
```

Astuce : on peut utiliser [`contextlib.closing`](https://docs.python.org/3/library/contextlib.html#contextlib.closing) pour le faire automatiquement et proprement

```python
from contextlib import closing
with closing(sqlite3.connect("db.sqlite3")) as con:
    pass  # Faire des trucs ici
```

Ok, super, on a ouvert et fermé un fichier, mais comment on accède à la base ?


Avec un [curseur](https://docs.python.org/3/library/sqlite3.html#cursor-objects)

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

Quelques trucs à noter

- On exécute des commands en SQL avec la méthode `execute` d'un curseur. On peut aussi exécuter tout un script avec `executescript` ou — mieux, voir plus bas — `executemany`
- Une fois qu'elles sont exécutées, il faut les valider en utilisant la méthode `commit` de la connexion. Tant qu'on ne l'a pas fait, rien ne se passe.
- Pour récupérer les résultats d'une requête on peut utilise les méthodes `fetchone`, `fetchall` ou `fetchmany` du curseur. Comme d'hab, la [doc](https://docs.python.org/3/library/sqlite3.html#cursor-objects) est votre amie.
- On ferme les curseurs avec leur méthode `close`


On peut récupérer un résumé de la table sous la forme des commandes SQL qui permettent de la recopier à l'identique avec `iterdump`

```python
with closing(sqlite3.connect("db.sqlite3")) as con:
    for l in con.iterdump():
        print(l)
```

Attention quand vous construisez des instructions SQL à partir d'entrées que vous ne maîtrisez pas

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

Pas de problème jusque là, mais si un individu malveillant passe un nom qui contient du code :

```python
read_recette("Tiramisu' or nom <> 'Tiramisu")
```

Ça dumpe toute la table ! Si vous avez eu la mauvaise idée de faire ça dans un `executescript` c'est pire, vous risquez de rencontrer Bobby Tables

[![](https://imgs.xkcd.com/comics/exploits_of_a_mom.png)](https://xkcd.com/327)


Pour éviter ça : on utilise des requêtes paramétrées qui seront asainies pour nous

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

Avec ça (et un manuel de SQL sous la main) vous avez l'essentiel de ce qu'il faut pour gérer des bases de données en SQLite. On l'a dit, c'est minimaliste.


Une dernière astuce ? On peut récupérer des mappings plutôt que des tuples avec `fetch…` :

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

## 🌲 Exo 🌲

Écrire un script qui construit une base de données en SQLite qui contient une table à trois colonnes qui représente un treebank Universal Dependencies. La première colonne qui servira de clé primaire contiendra pour chaque arbre son attribut `sent_id`, la deuxième contiendra son attribut `text`, enfin la dernière contiendra l'arbre syntaxique qu format CoNLL-U. Vous pouvez vous aider de [`conllu`](https://github.com/EmilStenstrom/conllu) pour faire le boulot de parser le fichier.
