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
Cours 12 : Itérateurs, générateurs et décorateurs
==================================================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

2021-10-20
<!-- #endregion -->

```python
from IPython.display import display
```

On ne va pas faire un cours sur la programmation fonctionnelle, mais je vous invite cependant à vous
intéresser à ce paradigme de programmation ou à jetter un œil au vénérable
[Lisp](https://fr.wikipedia.org/wiki/Lisp), à [Haskell](https://www.haskell.org/) ou (cocorico à)
[OCaml](https://ocaml.org/).

En Python tout est objet, ça vous le savez. Vous savez aussi que Python est un langage
multi-paradigme. Vous pouvez programmer dans un style procédural, en objet ou dans un style
fonctionnel.

Qu'est-ce que cela signifie un style fonctionnel ?

Vous ne pourrez pas produire de programmation fonctionnelle « pure » mais vous pouvez vous en
approcher en privilégiant les fonctions sans effet de bord (pas de changement d'état, par exemple
dans les structures de données), en évitant les variables globales, ou encore en utilisant des
fonctions d'ordre supérieur (c-a-d des fonctions qui acceptent des fonctions comme arguments ou qui
renvoient des fonctions).

Vous pouvez aussi apprendre à vous servir des itérateurs, des générateurs (ce qu'on fera ici) puis,
si vous voulez, aller plus loin avec les modules
[itertools](https://docs.python.org/3/library/itertools.html#module-itertools) et
[functools](https://docs.python.org/3/library/functools.html#module-functools)


```python
def fun(x):
    return 2*x
fun
```

## Les itérateurs

Itérer vous connaissez déjà : c'est ce qu'on fait avec une boucle `for`, ici pour une liste

```python
numbers = [1, 2, 3, 4, 5]
for it in numbers:
    print(it)
```

On peut faire ça avec tous les objets ?

```python
number = 5
for i in numbers:
    print(i)
```

Non.


Les objets sur lesquels on peut *itérer* sont des *itérables*. Ils doivent pour ça implémenter la
méthode `__iter__`, qui renvoie un *itérateur*.

```python
numbers = [1, 2, 3, 4, 5]
itr = numbers.__iter__()
type(itr)
```

Les itérateurs sont des objets qui représentent un flux de données. Pour être un itérateur un objet
doit implémenter la fonction `__next()__`. Cette fonction peut aussi s'appeler avec `next()`, elle
ne reçoit pas d'argument, renvoie le prochain élément, et si plus d'élément renvoie l'exception
`StopIteration`.

Voici un itérateur :

```python
itr = iter([2, 7, 1, 3])
display(type(itr))
```

La façon canonique de récupérer l'élément suivant

```python
a = next(itr)
a
```

À plus bas niveau, ce qui se passe, c'est

```python
a = itr.__next__()
a
```

Mais comme d'habitude, c'est mieux d'éviter d'appeler directement les dunders.

On continue ?

```python
next(itr)
```

Encore

```python
next(itr)
```

Et encore

```python tags=["raises-exception"]
next(itr)
```

Ah oui, on a fini.


Quand vous écrivez

```python
for i in [1, 2, 3, 4]:
    print(i)
```

Ce qui se passe en coulisse, c'est *grosso mode*

```python
itr = [1, 2, 3, 4].__iter__()
while True:
    try:
        a = next(itr)  # Qui appelle `itr.__next__()`
    except StopIteration:
        break
    print(a)
```

Un itérateur est un flux, vous pouvez accéder aux éléments les uns après les autres mais pas revenir
en arrière ou faire une copie. Si vous voulez accéder à nouveau au flux vous devez utiliser un
nouvel itérateur. C'est le cas pour la lecture d'un fichier par exemple : vous ne pouvez pas lire à
nouveau l'objet fichier si vous l'avez déjà fait.

Quel intérêt ? Et bien par exemple on peut avoir des itérateurs infinis, comme ceux renvoyés par `itertools.count()`.

```python
from itertools import count
for i in count():
    print(i)  # Décommentez pour le voir en action
    if i**2 > 18701871:
        break
print(f"Le premier nombre dont le carré dépasse 18701871 est {i}")
```

## Les générateurs


Les générateurs sont très simples à utiliser et très puissants. Ils vous permettront d'optimiser
votre code à moindre frais. Alors pourquoi se priver ?


Imaginons que je veuille extraire d'une liste de mots la liste des mots comportant le caractère
`'a'`. Je vais écrire une fonction.

```python
def with_a(words):
    """
    Reçoit une liste de mots et renvoie la liste des mots contenant le car. 'a'
    """
    res = []
    for word in words:
        if 'a' in word:
            res.append(word)
    return res
    
```

```python
mots = ["le", "petit", "chat", "est", "content", "ce", "matin"]
mots_a = with_a(mots)
for w in mots_a:
    print(w)
```

Rien de méchant.


On va mesurer le temps de traitement avec `%time`. <small>Jupyter est plein de magie, `%time` supercalifragilisticexpialidocious et voilà.</small>

```python
%time mots_a = with_a(mots)
mots_big = mots * 1000000
%time mots_a = with_a(mots_big)
```

Comme on pouvait s'y attendre le temps d'exécution de la fonction augmente avec la taille de la
liste initiale.


Essayons maintenant comme ça

```python
def gen_with_a(words):
    """
    Reçoit une liste de mots et renvoie les mots contenant le car. 'a' sous forme de générateur
    """
    for word in words:
        if 'a' in word:
            yield word
```

```python
mots = ["le", "petit", "chat", "est", "content", "ce", "matin"]
mots_a = gen_with_a(mots)
for w in mots_a:
    print(w)
```

Construire un générateur, c'est simple : vous remplacez `return` par `yield` dans votre fonction.

C'est tout ? C'est tout.  

<small>Vous pouvez quand même en apprendre plus en lisant la [PEP
255](https://www.python.org/dev/peps/pep-0255/) si vous aimez ça.</small>

Est-ce que ça va vite ?

```python
mots_big = mots * 1000000
%time mots_a = with_a(mots_big)
%time mots_a_gen = gen_with_a(mots_big)
```

![Mème « surprised Pikachu »](https://i.kym-cdn.com/entries/icons/original/000/027/475/Screen_Shot_2018-10-25_at_11.02.15_AM.png)

Oui, c'est de la magie. Enfin, c'est plutôt de la triche, regardez :

```python
print(f"mots_a is a {type(mots_a)}")
print(f"mots_a_gen is a {type(mots_a_gen)}")
import sys
print(f"Taille de mots_a : {sys.getsizeof(mots_a)}")
print(f"Taille de mots_a_gen : {sys.getsizeof(mots_a_gen)}")
```

`mots_a_gen` n'est pas une liste, c'est un objet `generator`.

Il ne stocke rien ou presque en mémoire, on ne peut pas connaître sa taille

```python tags=["raises-exception"]
len(mots_a_gen)
```

Mais on peut le parcourir comme une liste. Par contre on ne peut pas les "trancher", on ne peut pas
accéder à un élément d'index `i` comme pour une liste, et on ne peut le parcourir qu'une seule fois.


Ça rappelle les itérateurs !


C'est parce que c'en est un cas particuleir.

Les générateurs permettent de créer des itérateurs sans se fatiguer. Une fonction classique reçoit
des paramètres, calcule un truc avec et renvoie le résultat. Un générateur renvoie un itérateur qui
donne accès à un flux de données.

Concrètement, tant que vous n'appelez pas `next()`, aucun code n'est exécuté. Quand vous appelez
`next()`, le code est exécuté jusqu'à arriver à un `yield <bidule>`. À ce moment, l'itérateur
renvoie la valeur <bidule> et se met en pause jusqu'au prochain `next(), où il reprendra l'exécution
là où il s'est arrêté.

Comme tout itérateur vous pouvez le convertir en liste ou en tuple si vous voulez.

```python
%time mots_a_gen = list(gen_with_a(mots_big))
```

Mais même sans tricher les générateurs demeurent très efficaces. Vous aurez compris qu'il vous est
désormais chaudement recommandé de les utiliser.


Si vous voulez en savoir plus sur la cuisine du truc vous pouvez utiliser le module `inspect`. Je
vous conseille d'en lire la doc d'ailleurs
: [https://docs.python.org/3/library/inspect.html](https://docs.python.org/3/library/inspect.html)

```python tags=["raises-exception"]
import inspect

mots_a_gen = gen_with_a(mots)
print(mots_a_gen)
print(inspect.getgeneratorstate(mots_a_gen))
print(next(mots_a_gen))
print(inspect.getgeneratorstate(mots_a_gen))
print(next(mots_a_gen))
print(inspect.getgeneratorstate(mots_a_gen))
print(next(mots_a_gen))
```

```python
inspect.getgeneratorstate(mots_a_gen)
```

Vous pouvez aussi utiliser des générateurs en compréhension, à la manière des listes en compréhension : 

```python
[mot for mot in mots if 'a' in mot]
```

```python
(mot for mot in mots if 'a' in mot)
```

Un dernier exemple

```python
%%timeit
squares = [i**2 for i in range(100000)]
for s in squares:
    if s > 18701871:
        break
s
```

```python
%%timeit
squares = (i**2 for i in range(100000))
for s in squares:
    if s > 18701871:
        break
s
```

Ah, et je peux faire ça aussi

```python
%%timeit
squares = (i**2 for i in count())
for s in squares:
    if s > 18701871:
        break
s
```

Il se passerait quoi si j'essayais avec une liste en compréhension ?


## Encore un peu de fonctionnel : fonctions lambda, `map` et `filter`


`map`et `filter` sont typiquement des fonctions qui viennent des langages fonctionnels. Elles
renvoient toutes les deux des itérateurs.

- `map` permet d'appliquer un traitement sur chaque élément d'un itérable
- `filter` filtre les éléments d'un itérable en fonction d'une condition

Oui on peut faire tout ça avec les listes en compréhension. C'est même plus pythonique, vous allez
donc continuer à utiliser les listes en compréhension plutôt que `map` et `filter`.

```python
def carre(x):
    return x**2

numbers = [1, 2, 3, 4, 5]
for it in map(carre, numbers):
    print(it)
# ou aussi
list(map(carre, numbers))
```

```python
[it**2 for it in numbers] # so pythonic
```

```python
def is_even(x):
    return not x%2

for it in filter(is_even, numbers):
    print(it)
# ou aussi
list(filter(is_even, numbers))
```

```python
[it for it in numbers if is_even(it)]
```

C'est un peu fastidieux d'écrire ces petites fonctions pour utiliser `map` et `filter`. Avec les
fonctions lambda, Python offre un moyen d'écrire des petites fonctions, de leur passer des
paramètres et d'en faire des fonctions anonymes. Oui des fonctions anonymes, elles n'ont pas de nom
quoi. Encore un truc qui vient de la programmation fonctionnelle, on en utilise plein en JavaScript
par exemple.

```python
for it in map(lambda x: x**2, numbers):
    print(it)
```

Ici on a bien une fonction qui est paramètre d'une autre fonction (`map`). On utilise souvent des
fonctions lambda avec `sorted`, typiquement pour trier un dictionnaire par valeur comme vous le
savez.

```python
letters = {'a': 5, 'b': 2, 'c': 7, 'd':1, 'e':12}
for it, val in sorted(letters.items(), key=lambda item: item[1]):
    print(it, val)
```

## Les décorateurs


Les décorateurs ont été introduits avec la [PEP 318](https://www.python.org/dev/peps/pep-0318/) en
2003 dans la version 2.4 de Python.


Une fonction est un objet. Vous savez : en Python tout est objet. On peut passer une fonction en
paramètre d'une fonction. Une fonction peut renvoyer une fonction en valeur de retour.

```python
def salut():
    print("salut")

bonjour = salut # passage de la référence de l'objet (remember le cours sur les classes et les objets)
bonjour()
```

Avec un décorateur on va emballer une fonction pour ajouter des fonctionnalités. Un décorateur
reçoit en paramètre une fonction et l'emballe dans une autre.

```python
def deco(func):
    def wrapper():
        print("salut", end=" ")
        func()
    return wrapper

def name():
    print("Frédéric")

obj = deco(name)
obj()
```

La PEP 318 a introduit le symbole '@'. Ça permet d'avoir une syntaxe plus simple, du code plus
propre.

```python
@deco
def name():
    print("Frédéric")
    
obj = name
obj()
```

Ce décorateur ne sert à rien, on est d'accord. Voici un exemple plus parlant avec un décorateur pour
mesurer le temps d'exécution d'une fonction :

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        value = func(*args, **kwargs)
        end = time.perf_counter()
        run_time = end - start
        print(f"Finished {func.__name__} in {run_time} secs")
        return value

    return wrapper
```

```python
@timer
def doubled_and_add(num):
    res = sum([i*2 for i in range(num)])
    print(f"Result : {res}")

doubled_and_add(100000)
```

```python
doubled_and_add(1000000)
```

Pour la plupart des gens, *écrire* des décorateurs est assez rare. En revanche, il devient de plus
en plus courant d'avoir à en utiliser pour certaines bibliothèques (comme FastAPI), n'hésitez
donc pas à explorer davantage comment ils fonctionnent et ce qu'on peut faire avec (**beaucoup** de
choses).
