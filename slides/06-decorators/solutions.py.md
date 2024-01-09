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

<!-- #region slideshow={"slide_type": "skip"} -->
<!-- LTeX: language=fr -->
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
Décorateurs : solutions
======================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## ✏️ Exo ✏️

> 1\. Écrire une fonction `renvoi` qui prend en argument une chaîne de caractères et **renvoie** une
> salutation sur le modèle de la cellule ci-après.
>
> 2\. Écrire une fonction `affiche` qui prend en argument une chaîne de caractères et **affiche** la > même
> salutation, mais renvoie `None`.
>
> 3\. Écrire une fonction `porquenolosdos` à deux arguments qui affiche le premier et renvoie le
> deuxième.
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
def renvoi(s):
    return f"Salut, {s}!"
```

```python
assert renvoi("Fred") == "Salut, Fred!"
assert renvoi("Morgan") == "Salut, Morgan!"
assert renvoi("lzqrigoqizrgn") == "Salut, lzqrigoqizrgn!"
assert renvoi("") == "Salut, !"
```

```python slideshow={"slide_type": "subslide"}
def affiche(bidule):
    print(f"Salut, {bidule}!")
```

```python
assert affiche("Fred") == None
assert affiche("Morgan") == None
assert affiche("lzqrigoqizrgn") == None
assert affiche("") == None
```

```python slideshow={"slide_type": "subslide"}
def porquenolosdos(a, b):
    print(f"Salut, {a}!")
    return f"Salut, {b}!"
```

```python
assert porquenolosdos(0, 1) == 1
assert porquenolosdos(1, 0) == 0
assert porquenolosdos(None, "xy") == xy 
assert porquenolosdos([1, 2, 3], None) = None
```

<!-- #region slideshow={"slide_type": "slide"} -->
## 2️⃣ Exo 2️⃣

> Écrire un décorateur `do_twice` qui appelle deux fois la fonction décorée.
<!-- #endregion -->

```python
def do_twice(fun):
    def décorée():
        fun()
        fun()
    return décorée
```

On teste :

```python
@do_twice
def print_motto():
    print("Be excellent to each other.")

print_motto()
```

<!-- #region slideshow={"slide_type": "slide"} -->
## 😴 Exo 😴

> Réécrire le décorateur `not_during_the_night` afin de lui faire accepter n'importe quelle fonction
> en entrée.
<!-- #endregion -->

```python
from datetime import datetime

def not_during_the_night(func):
    def wrapper(*args, **kwargs):
        if 7 <= datetime.now().hour < 22:
            func(*args, **kwargs)
        else:
            pass  # Hush, the neighbors are asleep
    return wrapper

@not_during_the_night
def greetings(name):
    print(f"Greetings, {name}!")

greetings("Morgan")
```

<!-- #region slideshow={"slide_type": "slide"} -->
## 📑 Exo 📑

Écrire un décorateur `twice` qui fait renvoyer un tuple contenant deux fois la valeur de retour de
la fonction décorée.
<!-- #endregion -->

```python
def twice(fun):
    def aux(*args, **kwargs):
        out = fun(*args, **kwargs)
        return (out, out)
    return aux
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

## ⏳ Exo ⏳

> Modifier le décorateur `slow_down` pour lui faire prendre un paramètre `wait`, qui détermine le
> temps ajouté (avec `time.sleep`) à chaque appel de fonction.

```python
import functools
import time

def slow_down(wait=1):
    """Sleep given amount of seconds before calling the function"""
    def decorator_slow_down(func):
        @functools.wraps(func)
        def wrapper_slow_down(*args, **kwargs):
            time.sleep(wait)
            return func(*args, **kwargs)
        return wrapper_slow_down
    return decorator_slow_down

@slow_down(5)
def greet(n):
    print(f"Salut à toi, {n}.")

greet("Louise Michel")
```
