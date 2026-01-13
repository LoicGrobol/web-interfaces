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
      jupytext_version: 1.18.1
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- #region slideshow={"slide_type": "skip"} -->
<!-- LTeX: language=fr -->
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
Cours 6 : Fonctions avancées
===========================

**L. Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)
<!-- #endregion -->

*Ce cours est **très** largement inspiré du cours de *Real Python* « [*Primer on Python
Decorators*](https://realpython.com/primer-on-python-decorators/) »*, vous pouvez aller y jeter un
œil pour un regard légèrement différent et plus d'exemples.

```python
# Les imports se font **toujours** en début de notebook
import functools
import random
import time
from datetime import datetime
```

<!-- #region slideshow={"slide_type": "slide"} -->
On ne va pas faire un cours sur la programmation fonctionnelle, mais je vous invite cependant à vous
intéresser à ce paradigme de programmation ou à jeter un œil au vénérable
[Lisp](https://fr.wikipedia.org/wiki/Lisp), à [Haskell](https://www.haskell.org/), mais surtout à
**[OCaml](https://ocaml.org/)**.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Fonctions

En Python tout est objet, ça, vous le savez. Vous savez aussi que Python est un langage
multi-paradigme. Vous pouvez programmer dans un style procédural, en objet ou dans un style
fonctionnel.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
Qu'est-ce que cela signifie « un style fonctionnel » ? C'est un style de programmation où les objets
de bases sont les **fonctions** et où la conception d'un programme consiste en gros à établir un
graphe de routage des données entre ces fonctions.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
Ça a pour principal avantage de permettre d'utiliser des outils mathématiques puissants pour
analyser des programmes, afin de prouver leur *correction* ou leur sécurité, voire de les optimiser
automatiquement.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Pour rappel : en informatique, une **fonction**, c'est un fragment de programme (une série
d'instructions) autonome, à laquelle on peut passer des variables dites « arguments », et dont on
peut recevoir une valeur, dite « valeur de retour ». En voici une :
<!-- #endregion -->

```python
def double(x):
    return 2*x

double(3)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Une fonction peut aussi avoir des « effets de bords » ([*side
effects*](https://en.wikipedia.org/wiki/Side_effect_(computer_science))) : elle peut modifier l'état
général du système, par exemple en modifiant un fichier, en affichant du texte dans la console, en
activant un périphérique…

Par exemple, la fonction [`print`](https://realpython.com/python-print) renvoie toujours `None`,
mais elle produit des effets de bord, le plus [simple](https://realpython.com/python-print/) étant
d'afficher du texte.
<!-- #endregion -->

```python
print("spam")
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Dans les langages de programmation fonctionnelle cités plus haut, on a tendance à se méfier des
effets de bord, qui rendent l'exécution d'un programme moins prévisible, et donc plus difficile à
raisonner avec.

En Python, on a moins ce genre de scrupules.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Quelques exemples de plus

Une fonction sans arguments, avec une valeur de retour constante :
<!-- #endregion -->

```python
def const():
    return 1871

print(const())
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Une fonction sans arguments, avec une valeur de retour non-constante (essayez de l'appeler plusieurs
fois) :
<!-- #endregion -->

```python
def rand_fun():
    return random.random()

print(rand_fun())
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Une fonction sans arguments, avec un effet de bord :
<!-- #endregion -->

```python
def verb():
    print("Esclave est le prolétaire, esclave entre tous est la femme du prolétaire.")

verb()
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Est-ce qu'elle a une valeur de retour ? En Python, toujours :
<!-- #endregion -->

```python
ret = verb()
print(ret)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Une fonction qui se termine sans renvoyer explicitement de valeur à l'aide de `return` renvoie
implicitement `None` :
<!-- #endregion -->

```python
def hwat():
    if 2 < 1:
        return "Nope"

a = hwat()
print(a)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Une fonction avec un argument et un effet de bord :
<!-- #endregion -->

```python
def game(command):
    print(f"Sam says: '{command}'")

game("Say something we'll have to bleep.")
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Une fonction avec deux arguments et une valeur de retour :
<!-- #endregion -->

```python
def double_and_forget(a, b):
    return 2*a

print(double_and_forget(7, 2713))
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Non, on est pas obligé d'utiliser tous les arguments.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Une fonction avec deux arguments et… deux valeurs de retour ???!??! :
<!-- #endregion -->

```python
def double_and_pass(a, b):
    return 2*a, b

print(double_and_pass(7, 2713))
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Ce qui se passe : on renvoie bien une seule valeur, mais celle-ci est un tuple à deux éléments :
<!-- #endregion -->

```python
a = double_and_pass(7, 2713)
print(type(a))
```

<!-- #region slideshow={"slide_type": "subslide"} -->
On peut bien sûr passer comme argument le contenu d'une variable :
<!-- #endregion -->

```python
un_nombre = 1804
print(double_and_pass(un_nombre, 2713))
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Et appeler une fonction dans une autre fonction
<!-- #endregion -->

```python
def double_plus_deux(x):
    dbl = double(x)
    return dbl + 2

print(double_plus_deux)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Voire appeler la fonction elle-même (on parle de **récursivité**)
<!-- #endregion -->

```python
def rec(x):
    if x <= 0:
        return x
    else:
        prev = rec(x-1)
        return x + prev

print(rec(128))
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Ou ici, des fonctions **mutuellement récursives** pour implémenter une [suite de
Collatz](https://en.wikipedia.org/wiki/Collatz_conjecture)
<!-- #endregion -->

```python
def left(n):
    if n % 2 == 0:
        print(f"left {n}")
        left(n//2)
    elif n == 1:
        print(f"left: {n}")
        return
    else:
        right(n)

def right(y):
    if y % 2 == 1:
        print(f"rigth: {y}")
        right((3*y + 1)//2)
    elif y == 1:
        print(f"right: {y}")
        return
    else:
        left(y)

left(39)
```

<!-- #region slideshow={"slide_type": "slide"} -->
## ✏️ Exo ✏️

1\. Écrire une fonction `renvoi` qui prend en argument une chaîne de caractères et **renvoie** une
salutation sur le modèle de la cellule ci-après.

2\. Écrire une fonction `affiche` qui prend en argument une chaîne de caractères et **affiche** la
même salutation, mais renvoie `None`.

3\. Écrire une fonction `porquenolosdos` à deux arguments qui affiche le premier et renvoie le
deuxième.
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
def renvoi(s):
    pass
```

```python
assert renvoi("Fred") == "Salut, Fred!"
assert renvoi("Morgan") == "Salut, Morgan!"
assert renvoi("lzqrigoqizrgn") == "Salut, lzqrigoqizrgn!"
assert renvoi("") == "Salut, !"
```

```python slideshow={"slide_type": "subslide"}
def affiche(bidule):
    pass
```

```python
assert affiche("Fred") == None
assert affiche("Morgan") == None
assert affiche("lzqrigoqizrgn") == None
assert affiche("") == None
```

```python slideshow={"slide_type": "subslide"}
def porquenolosdos(a, b):
    pass
```

```python
assert porquenolosdos(0, 1) == 1
assert porquenolosdos(1, 0) == 0
assert porquenolosdos(None, "xy") == xy 
assert porquenolosdos([1, 2, 3], None) == None
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Jouer avec les arguments

Il arrive qu'on ne sache pas à l'avance quels arguments une fonction peut prendre, comme ici dans
`sum` :
<!-- #endregion -->

```python
sum(1, 2, 3)
```

```python
sum(1, 2, 3, 4, 5, 6)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
On dit que la fonction `sum` est **variadique**. Tous les langages de programmation ne le permettent
pas, parce qu'en pratique on peut toujours remplacer ça par une fonction qui prend une liste en
argument.
<!-- #endregion -->

```python
def my_sum(lst):
    res = 0
    for e in lst:
        res += e
    return res

my_sum([1, 2, 3, 4])
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Mais la syntaxe sans les doubles délimiteurs `([` est quand même agréable, du coup on peut utiliser
la syntaxe suivante.
<!-- #endregion -->

```python
def my_sum(*lst):
    res = 0
    for e in lst:
        res += e
    return res

my_sum(1, 2, 3, 4)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
`*lst` signifie « collecte les arguments qui n'ont pas été affectés et mets-les dans une liste ». On
peut donc avoir ça :
<!-- #endregion -->

```python
def varfun(head, *rest):
    print(f"head: {head}")
    print(f"rest: {rest}")

varfun(1, 2, 3, 4, 5)
print()
varfun(1)
```

(Tiens, ce n'est pas exactement une liste. C'est quoi ?)

<!-- #region slideshow={"slide_type": "subslide"} -->
Ça ne concerne par contre que les arguments *positionnels*, pas ceux *nommés* :
<!-- #endregion -->

```python
def varfun(a, *lst, bidule="truc"):
    print(f"a: {a}")
    print(f"lst: {lst}")
    print(f"bidule: {bidule}")

varfun(1,2,3,4,5)
print()
varfun(1,2,3,4,5, bidule="machin")
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Si on veut avoir des arguments variadiques nommés, on peut les récupérer comme ça :
<!-- #endregion -->

```python
def varfun(a, **d):
    print(f"a: {a}")
    print(f"d: {d}")

varfun(1, machin=1, truc="bidule")
print()
varfun("abc")
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Et on peut combiner les deux :
<!-- #endregion -->

```python
def varfun(a, *l, **d):
    print(f"a: {a}")
    print(f"l: {l}")
    print(f"d: {d}")

varfun(1, 2, 3, machin=1, truc="bidule")
print()
varfun("abc")
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Réciproquement, si vous disposez de listes ou de dictionnaires, vous pouvez les passer à votre
fonction comme si c'étaient des arguments :
<!-- #endregion -->

```python
def fun(a, b, c):
    print(f"a: {a}")
    print(f"b: {b}")
    print(f"c: {c}")

l = [1, 2, 3]
fun(*l)

print()

l = [1, 2]
fun("xyz", *l)
print()
fun(*l, "xyz")
```

```python slideshow={"slide_type": "slide"}
def fun(a, truc, chose):
    print(f"a: {a}")
    print(f"truc: {truc}")
    print(f"chose: {chose}")

# Attention les clés du dictionnaires doivent alors être des str
d = {"truc": 1, "chose": "abc"}
fun(12, **d)

print()

d = {"a": -6, "truc": 1, "chose": "abc"}
fun(**d)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Et même combiner tout ça (en pratique allez y doucement, ça rend vite le code illisible) :
<!-- #endregion -->

```python
def fun(a, b, *args, **kwargs):
    print(a, b, args, kwargs)

fun(1, 2, 3, 4, 5, 6, truc=-2, machin="chose")
```

Pour plus de détails sur cette syntaxe, vous ~~pouvez~~ devez consulter [la doc pour la syntaxe des
définitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions) et des
[appels](https://docs.python.org/3/reference/expressions.html#calls) de fonction, et la présentation
plus pédagogique de [Real Python](https://realpython.com/python-kwargs-and-args/).

<!-- #region slideshow={"slide_type": "slide"} -->
## Des citoyennes de première classe

En Python, les fonctions sont des objets manipulables comme les autres, on dit que ce sont
des « *first class citizens* ». Elles peuvent être affectées à des variables :
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
fois_deux = double
fois_deux(3)
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Ou être passées en argument à d'autres fonctions :
<!-- #endregion -->

```python
def interface(operation_fun):
    nombre = operation_fun(7)
    print(f"Appliquer cette fonction à 7 donne {nombre}")

interface(double)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Un autre exemple :
<!-- #endregion -->

```python
def rufus(name):
    return f"Greetings, {name}"

def bill(name):
    return f"Yo {name}, together we are most excellent!"

def greet_ted(greeter_func):
    return greeter_func("Ted")
```

```python
print(greet_ted(rufus))
```

```python
print(greet_ted(bill))
```

<!-- #region slideshow={"slide_type": "subslide"} -->
## Fonctions imbriquées

Les fonctions sont **vraiment** des objets comme les autres. On peut donc tout à fait définir une
fonction à l'intérieur d'une autre fonction :
<!-- #endregion -->

```python
def parent():
    print("Printing from the `parent` function")

    def first_child():
        print("Printing from the `first_child` function")

    def second_child():
        print("Printing from the `second_child` function")

    second_child()
    first_child()
```

Avant d'aller plus loin, réfléchissez quelques instants à ce qui va se passer si on appelle
`parent`.

<!-- #region slideshow={"slide_type": "subslide"} -->
Maintenant, testez :
<!-- #endregion -->

```python
parent()
```

Vous pouvez aussi visualiser l'exécution en utilisant le débuggueur de Jupyter ou sur [Python
Tutor](https://pythontutor.com/render.html#code=def%20parent%28%29%3A%0A%20%20%20%20print%28%22Printing%20from%20the%20parent%28%29%20function%22%29%0A%0A%20%20%20%20def%20first_child%28%29%3A%0A%20%20%20%20%20%20%20%20print%28%22Printing%20from%20the%20first_child%28%29%20function%22%29%0A%0A%20%20%20%20def%20second_child%28%29%3A%0A%20%20%20%20%20%20%20%20print%28%22Printing%20from%20the%20second_child%28%29%20function%22%29%0A%0A%20%20%20%20second_child%28%29%0A%20%20%20%20first_child%28%29%0A%20%20%20%20%0Aparent%28%29&cumulative=false&curInstr=15&heapPrimitives=nevernest&mode=display&origin=opt-frontend.js&py=311&rawInputLstJSON=%5B%5D&textReferences=false)

<!-- #region slideshow={"slide_type": "subslide"} -->
Quelques notes :

- L'ordre dans lequel les fonctions enfant sont **définies** n'a pas d'importance : leur code n'est
  exécuté que quand elles sont **appelées**. À la définition, il est simplement *analysé*.
<!-- #endregion -->

```python
def parent():
    print("Printing from the `parent` function")

    def second_child():
        print("Printing from the `second_child` function")

    def first_child():
        print("Printing from the `first_child` function")

    second_child()
    first_child()

parent()
```

<!-- #region slideshow={"slide_type": "subslide"} -->
- Les fonctions enfant ne sont définies qu'à l'intérieur de la fonction parent. Jamais à
  l'extérieur, ni avant, ni après.
<!-- #endregion -->

```python
def parent():
    def child():
        print("Yo")
    child()  # Ceci est OK

parent()
```

```python tags=["raises-exception"]
child()  # Pas ceci
```

```python tags=["raises-exception"]
parent()
child()  # Ni celà
```

<!-- #region slideshow={"slide_type": "subslide"} -->
- Les fonctions enfant ont accès aux variables accessibles dans la fonction parent, on dit que ce
  sont des *fermetures* (en:*closures*) :
<!-- #endregion -->

```python
def parent():
    s = 1
    def child():
        print(s)
    child()

parent()
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Renvoyer des fonctions

**Les fonctions sont des objets comme les autres**, une fonction peut donc renvoyer une fonction.
<!-- #endregion -->

```python
def ret_print():
    return print  # On renvoie une **référence** à la fonction `print`

a = ret_print()
a("Hello, world!")
```

```python slideshow={"slide_type": "fragment"}
ret_print()("spam")
```

```python slideshow={"slide_type": "fragment"}
print(ret_print())
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Attention à ne pas confondre :
<!-- #endregion -->

```python tags=["raises-exception"]
def ret_quoi():
    return print()

a = ret_quoi()
a("Hello, world!")
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Vous voyez la différence ?
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
print(a)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Évidemment, c'est plus intéressant si la fonction qu'on renvoie n'est pas toujours la même :
<!-- #endregion -->

```python
def parent(num):
    def first_child():
        return "Hi, I am Fañch"

    def second_child():
        return "Call me Liam"

    if num == 1:
        return first_child
    else:
        return second_child

first = parent(1)
second = parent(2)
```

```python
print(first)
```

```python
print(second)
```

```python slideshow={"slide_type": "subslide"}
first()
```

```python
second()
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Et comme **les fonctions sont des objets comme les autres**, on peut prendre une fonction en
argument et renvoyer une fonction :
<!-- #endregion -->

```python
def log(func):
    def sub():
        print("Attention, je vais faire un truc!")
        func()
        print("Voilà, j'ai fait un truc!")
    return sub

def say_whee():
    print("Whee!")

f = log(say_whee)
```

À votre avis, il se passe quoi si j'appelle `f` ?

```python slideshow={"slide_type": "fragment"}
f()
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Une fonction comme `log`, qui prend une fonction en entrée et renvoie une fonction en sortie est
parfois appelée *fonction d'ordre supérieur*, *opérateur* ou *fonctionnelle*. On rencontre aussi
*foncteur*, qui est un usage un peu abusif.

On dit aussi que la fonction `f`, qui contient une exécution de `func` et lui ajoute d'autres
instructions, est une version *décorée* de `func` (on lui a mis des guirlandes, quoi, c'est la
saison), et par conséquent que `log` est un *décorateur*.

Si on aime bien la typologie : en principe un décorateur est toujours une fonction d'ordre
supérieur, mais une fonction d'ordre supérieur n'est pas forcément un décorateur. En pratique le
concept de décorateur en Python est étendu à d'autres techniques, ce qui rend la distinction moins
claire.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Redisons le plus simplement :

> Un décorateur est une fonction qui modifie le comportement d'une autre fonction

Voici un autre exemple :
<!-- #endregion -->

```python
def not_during_the_night(func):
    def wrapper():
        if 9 <= datetime.now().hour < 17:
            func()
        else:
            pass  # Hush, the sun is down
    return wrapper

def say_whee():
    print("Whee!")

say_whee_decorated = not_during_the_night(say_whee)
```

Essayez d'exécuter la cellule suivante ce soir

```python
say_whee_decorated()
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Notez que si on écrivait `say_whee = not_during_the_night(say_whee)`, on a définitivement changé la
valeur de la **variable** `say_whee`, qui ne contient plus la fonction de départ, mais la fonction
décorée.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## You can keep your `@` on

La syntaxe précédente `say_whee = not_during_the_night(say_whee)` est un peu désagréable : déjà
c'est long à écrire, et puis on définit un truc pour l'effacer tout de suite après, ce qui n'est pas
très satisfaisant.

À la place Python propose une simplification d'écriture. Du « sucre syntaxique » défini par la [PEP
318P](https://peps.python.org/pep-0318/#background) :
<!-- #endregion -->

```python
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator #  ← voyez comme c'est sucré
def say_whee():
    print("Whee!")

say_whee()
```

Ici, ajouter `@my_decorator` avant une définition de fonction, c'est exactement équivalent à écrire
`say_whee = my_decorator(say_whee)`.

<!-- #region slideshow={"slide_type": "slide"} -->
## 2️⃣ Exo 2️⃣

Écrire un décorateur `do_twice` qui appelle deux fois la fonction décorée.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Décorer des fonctions avec des arguments

Imaginons, tout à fait au hasard le décorateur suivant :
<!-- #endregion -->

```python
def do_thrice(fun):
    def aux():
        fun()
        fun()
        fun()
    return aux
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Appliquons-le à une fonction simple :
<!-- #endregion -->

```python
@do_thrice
def greet_ted():
    print(f"Greetings, Ted")

greet_ted()
```

```python
@do_thrice
def greet(name):
    print(f"Greetings, {name}")
```

```python tags=["raises-exception"]
greet("Bill")
```

Que se passe-t-il si vous exécutez la cellule précédente ?

<!-- #region slideshow={"slide_type": "subslide"} -->
Le problème, c'est que `aux`, la fonction décorée, ne prend pas d'argument. C'est donc une erreur de
lui en passer un. Il faut donc prévoir de faire transiter les arguments :
<!-- #endregion -->

```python
def do_thrice(fun):
    def aux(s):
        fun(s)
        fun(s)
        fun(s)
    return aux

@do_thrice
def greet(name):
    print(f"Greetings, {name}")

greet("Bill")
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Et si on ne sait pas à l'avance quels arguments va prendre la fonction qui sera décorée ? On peut
utiliser des arguments variadiques comme ça :
<!-- #endregion -->

```python
def do_thrice(fun):
    def aux(*args, **kwargs):
        fun(*args, **kwargs)
        fun(*args, **kwargs)
        fun(*args, **kwargs)
    return aux

@do_thrice
def greet(name):
    print(f"Greetings, {name}")

@do_thrice
def greet_ted():
    print("Greetings to you, Ted")

greet("Bill")
greet_ted()
```

Ça veut dire que quel que soient les arguments passés à `do_thrice`, ils seront repassés à `fun` tel
quel. Par convention, on note `*args` les arguments positionnels et `**kwargs` les `keywords`.

<!-- #region slideshow={"slide_type": "slide"} -->
## 😴 Exo 😴

Réécrire le décorateur `not_during_the_night` afin de lui faire accepter n'importe quelle fonction
en entrée.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Renvoyer une valeur depuis une fonction décorée

Et pour les valeurs de retour des fonctions décorées ? Voyons :
<!-- #endregion -->

```python
def log(func):
    def sub(*args, **kwargs):
        print("Attention, je vais faire un truc!")
        func(*args, **kwargs)
        print("Voilà, j'ai fait un truc!")
    return sub

@log
def return_greeting(name):
    print("Creating greeting")
    return f"Greetings, {name}"
```

```python
hi_ted = return_greeting("Ted")
print(hi_ted)
```

La fonction décorée ne renvoie rien. C'est normal : on ne lui a rien fait renvoyer. Ça doit être
fait explicitement :

```python slideshow={"slide_type": "subslide"}
def log(func):
    def sub(*args, **kwargs):
        print("Attention, je vais faire un truc!")
        res = func(*args, **kwargs)
        print("Voilà, j'ai fait un truc!")
        return res
    return sub

@log
def return_greeting(name):
    print("Creating greeting")
    return f"Greetings, {name}"

hi_ted = return_greeting("Ted")
print(hi_ted)
```

<!-- #region slideshow={"slide_type": "slide"} -->
## 📑 Exo 📑

Écrire un décorateur `twice` qui fait renvoyer un tuple contenant deux fois la valeur de retour de
la fonction décorée.
<!-- #endregion -->

```python
def twice(fun):
    pass
```

Testez votre réponse avec la cellule suivante.

```python slideshow={"slide_type": "subslide"}
def identity(x):
    return x

def double(x):
    return 2*x

assert twice(identity)(2) == (2, 2)
assert twice(double)(4) == (8, 8)

@twice
def spam():
    return "spam"

assert spam() == ("spam", "spam")
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Une question d'identité

Une fonction en Python transporte avec elle des métadonnées :
<!-- #endregion -->

```python
print
```

```python
print(print.__name__)
```

```python
help(print)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Et pour les fonctions décorées ?
<!-- #endregion -->

```python
return_greeting
```

```python
return_greeting.__name__
```

```python
help(return_greeting)
```

Le décorateur a absorbé les informations de la fonction de base et ne veut pas les rendre !

<!-- #region slideshow={"slide_type": "subslide"} -->
Pour éviter ça, on peut utiliser le **décorateur** (!)
[`@functools.wraps`](https://docs.python.org/library/functools.html#functools.wraps) :
<!-- #endregion -->

```python
def log(func):
    @functools.wraps(func)
    def sub(*args, **kwargs):
        print("Attention, je vais faire un truc!")
        res = func(*args, **kwargs)
        print("Voilà, j'ai fait un truc!")
        return res
    return sub

@log
def return_greeting(name):
    print("Creating greeting")
    return f"Greetings, {name}"
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Voyons ce que ça donne :
<!-- #endregion -->

```python
return_greeting
```

```python
return_greeting.__name__
```

```python
help(return_greeting)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Si on veut écrire des décorateurs, c'est une bonne pratique importante d'utiliser
`@functools.wraps`, à moins d'avoir une raison vraiment **très** importante de faire autrement.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Quelques exemples
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Chronométrer une fonction :
<!-- #endregion -->

```python
def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer

@timer
def waste_some_time(num_times):
    for _ in range(num_times):
        sum([i**2 for i in range(10000)])
```

```python
waste_some_time(1)
```

```python
waste_some_time(999)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Espionner une fonction :
<!-- #endregion -->

```python
def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")           # 4
        return value
    return wrapper_debug
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Testons :
<!-- #endregion -->
```python
@debug
def make_greeting(name, age=None):
    if age is None:
        return f"Howdy {name}!"
    else:
        return f"Whoa {name}! {age} already, you are growing up!"
```

```python
make_greeting("Benjamin")
```

```python
make_greeting("Richard", age=112)
```

```python
make_greeting(name="Dorrisile", age=116)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Reprenons nos fonctions mutuellement récursives de tout à l'heure :
<!-- #endregion -->

```python
@debug
def left(n):
    if n % 2 == 0:
        print(n)
        left(n//2)
    elif n == 1:
        print(n)
        return
    else:
        right(n)

@debug
def right(y):
    if y % 2 == 1:
        print(y)
        right((3*y + 1)//2)
    elif y == 1:
        print(y)
        return
    else:
        left(y)

left(39)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### Ralentir une fonction
<!-- #endregion -->

```python
def slow_down(func):
    """Sleep 1 second before calling the function"""
    @functools.wraps(func)
    def wrapper_slow_down(*args, **kwargs):
        time.sleep(1)  # Attendre une seconde
        return func(*args, **kwargs)
    return wrapper_slow_down

@slow_down
def countdown(from_number):
    if from_number < 1:
        print("Liftoff!")
    else:
        print(from_number)
        countdown(from_number - 1)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Voir les autres exemples sur [Real
Python](https://realpython.com/primer-on-python-decorators/#a-few-real-world-examples).
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Combiner des décorateurs

On peut appliquer plusieurs décorateurs à la suite :
<!-- #endregion -->

```python
@debug
@do_thrice
def greet(name):
    print(f"Greetings, {name}!")

greet("Bill")
```

C'est équivalent à `greet = debug(do_thrice(greet))`

<!-- #region slideshow={"slide_type": "subslide"} -->
Du coup l'ordre est significatif ! Observez la différence :
<!-- #endregion -->

```python
@do_twice
@debug
def greet(name):
    print(f"Hello {name}")

greet("Bill")
```

<!-- #region slideshow={"slide_type": "subslide"} -->
## Décorateurs paramétrés

C'est souvent utile d'avoir des décorateurs qui prennent eux-mêmes des paramètres. Par exemple
pensez à `do_twice` et `do_thrice` qu'on a vu précédemment. Ils font la même chose (répéter la
fonction qu'ils décorent), la seule différence était le nombre de répétitions. Ça serait bien si on
avait un décorateur générique façon `do_n` pour lequel on choisirait à chaque fois `n`, le nombre de
répétitions.

Pour ça, on va devoir compliquer un peu les choses et faire en sorte que `do_n` soit une fonction
qui elle-même renvoie un décorateur :
<!-- #endregion -->

```python
def do_n(n):
    def decorate(fun)
        @functools.wraps
        def aux(*args, **kwargs):
            # Underscore par convention, parce que la valeur n'est pas utilisée
            for _ in range(n):  
                fun(*args, **kwargs)
        return aux
    return decorate

def greet(name):
    print(f"Hello {name}")

do_n(5)(greet)("Bill")
```

Ça fait beaucoup d'imbrications, mais ce n'est pas si compliqué quand on prend les choses une par
une.

<!-- #region slideshow={"slide_type": "subslide"} -->
Ceci est la fonction après décoration : on a `n` et `fun`, la fonction à décorer ; on appelle
simplement `n` fois `fun`.

```python
def aux(*args, **kwargs):
    # Underscore par convention, parce que la valeur n'est pas utilisée
    for _ in range(n):  
        fun(*args, **kwargs)
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Ceci est le décorateur : il dispose déjà de `n`, et si on lui donne une fonction, il la décore

```python
def decorate(fun)
        @functools.wraps
        def aux(*args, **kwargs):
            ...
        return aux
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Ceci génère des décorateurs : on lui donne un `n` et il renvoie un décorateur, qui peut alors être
utilisé pour décorer des fonctions.

```python
def do_n(n):
    def decorate(fun)
        ...
    return decorate
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Quand on appelle `do_n(5)(greet)("Bill")`, il se passe donc ceci
<!-- #endregion -->

```python
decorator = do_n(5)  # On créé un décorateur
decorated = decorator(greet)  # On décore `greet`
decorated("Bill")  # On appelle la fonction décorée.
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Et pour utiliser la syntaxe `@` ? Simplement comme ceci :


```python
@do_n(6)
def greet(name):
    print(f"Hello {name}")

greet("Bill")
```

<!-- #region slideshow={"slide_type": "slide"} -->
## ⏳ Exo ⏳

Modifier le décorateur `slow_down` pour lui faire prendre un paramètre `wait`, qui détermine le
temps ajouté (avec `time.sleep`) à chaque appel de fonction.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Et après

Allez lire [le tuto de Real
Python](https://realpython.com/primer-on-python-decorators/#fancy-decorators). Vous y apprendrez par
exemple à écrire des décorateurs pour des classes (oui, comme `@dataclass`).
<!-- #endregion -->
