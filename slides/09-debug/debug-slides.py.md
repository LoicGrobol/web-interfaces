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

<!-- #region slideshow={"slide_type": "slide"} -->
<!-- LTeX: language=fr -->
Cours 08 : Débuggueurs, formatteurs et linters
==============================================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Traceback

Parfois rien ne marche, y a des jours comme ça
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"} tags=["raises-exception"]
def catchy_song(animal):
    print(f"I got a {anmal} in my living room")

catchy_song("llama")
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Heureusement, notre ami Python nous dit où ça ne va pas : et affiche un *traceback*

```traceback
NameError     Traceback (most recent call last)
/tmp/ipykernel_74898/3387701961.py in <module>
      2     print(f"There's a {anmal} in my living room")
      3 
----> 4 catchy_song("llama")

/tmp/ipykernel_74898/3387701961.py in catchy_song(animal)
      1 def catchy_song(animal):
----> 2     print(f"There's a {anmal} in my living room")
      3 
      4 catchy_song("llama")

NameError: name 'anmal' is not defined
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
C'est bien pratique : on voit tout de suite le problème :

- La dernière ligne `NameError: name 'anmal' is not defined` nous dit exactement ce qui pose le
  problème
- Le reste nous dit où il se trouve et comment on est arrivé⋅e⋅s là. De haut en bas on a la fonction
  où se trouve le problème, puis la fonction qui l'appellée et ainsi de suite
- On parle de *pile d'appels*
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Et on peut corriger
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
def catchy_song(animal):
    print(f"There's a {animal} in my living room")

catchy_song("llama")
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Pensez à aller voir [la doc](https://docs.python.org/library/exceptions.html) si vous ne comprenez
pas l'erreur que vous recevez.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Malheureusement, quand le code ne fait ce qu'on veut, il n'a pas toujours la décence de planter.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Factorielle

**Rappel** la fonction « factorielle » est définie par

$$\text{factorielle}(n) = 1×2×…×n$$
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
import math
math.factorial(9)
```

**Exercice** écrire une fonction `factorial` qui calcule la factorielle d'un nombre

```python
def factorial(n):
    if n == 0:
        return 1
    pass  # À vous !
```

```python slideshow={"slide_type": "subslide"}
def factorial(n):
    if n == 0:
        return 1
    res = 1
    for i in range(1, n):
        res = i * res
    return res

factorial(9)
```

<!-- #region slideshow={"slide_type": "fragment"} -->
On a clairement un problème, mais où ?
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Pour le savoir on peut par exemple insérer un `print` dans la boucle pour voir ce qui se passe
pendant l'exécution.
<!-- #endregion -->

```python
def factorial(n):
    if n == 0:
        return 1
    res = 1
    for i in range(1, n):
        print(i, res)
        res = i * res
    return res
    
factorial(9)
```

Alors, quel est le problème ? Comment on corrige ?

```python slideshow={"slide_type": "subslide"}
for n in range(10):
    print(n, math.factorial(n))
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Voilà la bonne version
<!-- #endregion -->

```python
def factorial(n):
    if n == 0:
        return 1
    res = 1
    for i in range(1, n+1):
        res = i * res
    return res
    
factorial(9)
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Un peu de textométrie

**Hypothèse** on veut savoir étant donné un mot, quels sont les mots qui apparaissent le plus
souvent dans la même phrase.

On travaille sur un « gros » corpus
<!-- #endregion -->

```python
!head ancor.txt
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Extrayons son vocabulaire

**Exercice** écrire une fonction `vocab` qui prend en argument un chemin vers un fichier texte et
qui renvoie

- Une liste contenant les mots du vocabulaire du texte
- Un `dict` qui mappe les mots vers leur position dans la liste
<!-- #endregion -->

```python
def vocab(f_path):
    i2t = []
    t2i = dict()
    with open(f_path) as in_stream:
        pass  # Faire des trucs ici

    return t2i, i2t
```

```python slideshow={"slide_type": "subslide"}
def vocab(f_path):
    i2t = []
    t2i = dict()
    with open(f_path) as in_stream:
        for l in in_stream:
            for word in l.strip().split():
                if word not in t2i:
                    t2i[word] = len(i2t)
                    i2t.append(word)
    return t2i, i2t

ancor_t2i, ancor_i2t = vocab("ancor.txt")
display(ancor_i2t)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
On construit sa matrice de cooccurrences

**Exercice** écrire une fonction `cooc` qui prend en argument un chemin vers un fichier texte et un
dict `{mot: indices}` et qui renvoie la matrice de coocurrences : une liste de listes telle que
`cooc[i][j]` est le nombre de fois que les mots `i` et `j` apparaissent dans une même phrase (on
suppose que ligne == phrase).
<!-- #endregion -->

```python
def cooc(f_path, t2i):
    pass
```

```python slideshow={"slide_type": "subslide"}
def cooc(f_path, t2i):
    cooc = [[0]*len(t2i)]*len(t2i)
    with open(f_path) as in_stream:
        for l in in_stream:
            words = l.strip().split()
            word_indices = [t2i[w] for w in words]
            for w in word_indices:
                cooc_w = cooc[w]
                for other in word_indices:
                    cooc_w[other] += 1
    return cooc

ancor_cooc = cooc("ancor.txt", ancor_t2i)
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Où on peut par exemple récupérer les $k$ mots qui apparaissent le plus souvent dans le contexte d'un
mot donné

**Exercice** écrire une fonction `arg_k_max` qui renvoie les indices des $k$ plus grands éléments
d'une liste.
<!-- #endregion -->

```python
def arg_k_max(lst, k):
    """Renvoie les indices des k plus grands éléments de `lst`"""
    res = []
    # Faire des trucs ici
    return res

arg_k_max([9, 10, 2, 3], k=2)
```

```python slideshow={"slide_type": "subslide"}
def arg_k_max(lst, k):
    """Renvoie les indices des k plus grands éléments de `lst`"""
    srt = sorted(enumerate(lst), key=(lambda x: x[1]), reverse=True)
    k_largest = srt[:k]
    return [i for i, _ in k_largest]

arg_k_max([9, 10, 2, 3], k=2)
```
<!-- #region slideshow={"slide_type": "subslide"} -->
Ou si les boucles c'est votre passion
<!-- #endregion -->

```python slideshow={"slide_type": "fragment"}
def arg_k_max(lst, k):
    """Renvoie les indices des k plus grands éléments de `lst`"""
    res = [] 
    for ո, val in enumerate(lst):
        if len(res) < k:
            res.append((n, val))
            res.sort(reverse=True, key=lambda x: x[1])
        elif res[-1][1] < val:
            res.pop()
            res.append((n, val))
            res.sort(reverse=True, key=lambda x: x[1])
    return [i for i, _ in res]

    arg_k_max([9, 10, 2, 3], k=2)
```

**Note** Si les performances sont importantes, préférer
[`heapq.nlargest`](https://docs.python.org/3/library/heapq.html#heapq.nlargest) pour sélectionner
les $k$ plus grands éléments d'une liste.

```python slideshow={"slide_type": "subslide"}
def common_neighbours(word, t2i, i2t, cooc, k=10):
    context = cooc[t2i[word]]
    k_largest = arg_k_max(context, k)
    return [i2t[index] for index in k_largest]

display(common_neighbours("moi", ancor_t2i, ancor_i2t, ancor_cooc))
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Il y a l'air d'avoir un problème.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
On pourrait faire des `print` mais il y a beaucoup de lignes, ça risque d'être long.

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Pyflakes à la rescousse
<!-- #endregion -->

On va utilise [`pyflakes`](https://pypi.org/project/pyflakes/), pensez à l'installer avec `pip`
avant de lancer la cellule suivante.

```python
!pyflakes lintme.py
```

[`lintme.py`](lintme.py) contient les fonctions qu'on a défini précédemment, allez voir ce qu'il y a
dans les lignes 31 et 35.


Est-ce que vous voyez le problème ?

<!-- #region slideshow={"slide_type": "subslide"} -->
Le problème est là

```python
for ո, val in enumerate(lst):
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
Juste ici

```text
for ո, val in enumerate(lst):
    ^
```
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
ord("n")
```

```python slideshow={"slide_type": "fragment"}
ord("ո")
```

<small>Jeu : trouver comment j'ai fait pour que ça ne fasse pas de NameError</small>

<!-- #region slideshow={"slide_type": "subslide"} -->
Voilà la bonne version
<!-- #endregion -->

```python
def arg_k_max(lst, k):
    """Renvoie les indices des k plus grands éléments de `lst`"""
    res = []
    for n, val in enumerate(lst):
        if len(res) < k:
            res.append((n, val))
            res.sort(reverse=True, key=lambda x: x[1])
        elif res[-1][1] < val:
            res.pop()
            res.append((n, val))
            res.sort(reverse=True, key=lambda x: x[1])
    return [i for i, _ in res]
```

<!-- #region slideshow={"slide_type": "subslide"} -->
### Nos amis les linters

Un *linter* c'est un outil d'analye **statique** du code.

Ça signifie qu'il n'exécute pas (et ne compile pas) votre code, il se contente de le lire pour
essayer de trouver vos erreurs.

C'est particulièrement utile quand on a du code qui est long à compiler (coucou le C) : on a pas
envie de perdre une heure pour apprendre qu'on a fait une faute de frappe.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
En général un linter vérifie au moins

- Que votre code est syntaxiquement correct
- Que toutes les variables déclarées sont utilisées
- Que toutes les variables utilisées sont déclarées
- Que les fonctions sont appellées avec des paramètres cohérents (en nombre, en noms…)
<!-- #endregion -->

Pylint se limite grosso modo à ces fonctions de base, mais il y en a d'autres plus complets.

<!-- #region slideshow={"slide_type": "slide"} -->
### PEP8 style

Essayons de lancer [`flake8`](http://flake8.pycqa.org) sur `lintme.py`
<!-- #endregion -->

```python
!flake8 lintme.py
```

<!-- #region slideshow={"slide_type": "subslide"} -->
`flake8` combine des fonctions de linter (en fait exactement celles de `pyflakes`) et de vérifieur
de styles plus d'autres (allez lire la doc).

En l'occurence il nous dit que la [PEP 8](https://www.python.org/dev/peps/pep-0008) qui définit le
style recommandé pour Python n'est pas respectée par la ligne suivante :

```python
cooc = [[0]*len(t2i)]*len(t2i)
```

qui devrait être

```python
cooc = [[0] * len(t2i)] * len(t2i)
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### [Black](https://www.youtube.com/watch?v=D_JxMb8RLEY)

Au siècle dernier, je vous aurait fait corriger des lignes de code à la main jusqu'à ce que
`flake8` cesse de se plaindre.
<!-- #endregion -->

Mais on est en 2021 et on a inventé mieux.

<!-- #region slideshow={"slide_type": "fragment"} -->
Meet [`black`](https://pypi.org/project/black)
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
**Avant**
<!-- #endregion -->

```python
!cat ugly.py
```

<!-- #region slideshow={"slide_type": "subslide"} -->
**Après**
<!-- #endregion -->

```python
!cat ugly.py | black -q -
```

<!-- #region slideshow={"slide_type": "subslide"} -->
`black` reformate vos fichiers de sorte qu'ils respectent la PEP 8, tout en se conformant à des
règles de style strictes.

On dit que `black` est un *formatteur de code*.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
Par choix, `black` n'est presque pas configurable : ça évite d'avoir à tergiverser sur les
conventions à adopter.

Si vous n'avez pas d'opinion précise sur comment votre code doit être, utilisez `black`, si vous
n'aimez pas les sorties de `black`, persévérez, on s'habitue.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
Si **vraiment** vous avez des goûts sophistiqués, il existe beaucoup d'autre formatteurs: par
exemple autopep8, yapf, rope…
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Pour une utilisation en console, lancez `black` comme

```bash
black monfichiermoche.py
```

Il le formatte en direct et sauvegarde. **Il modifie votre fichier, attention**.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "fragment"} -->
Plus agréablement : `black` et `flake8` sont intégrés à la plupart des éditeurs et IDEs, n'hésitez
pas à les utiliser en permanence, vous vous remercierez dans six mois.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Enfin libres

Ah, c'est bon d'avoir du code qui marche
<!-- #endregion -->

```python
display(common_neighbours("moi", ancor_t2i, ancor_i2t, ancor_cooc))
```

<!-- #region slideshow={"slide_type": "subslide"} -->
Enfin, on a fini, la fonction marche, on peut l'appliquer à ce qu'on veut
<!-- #endregion -->

```python
display(common_neighbours("bonjour", ancor_t2i, ancor_i2t, ancor_cooc))
```

```python slideshow={"slide_type": "subslide"}
display(common_neighbours("Russie", ancor_t2i, ancor_i2t, ancor_cooc))
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Euh
<!-- #endregion -->

```python slideshow={"slide_type": "subslide"}
display(common_neighbours("Orléans", ancor_t2i, ancor_i2t, ancor_cooc))
```

```python
display(common_neighbours("médecin", ancor_t2i, ancor_i2t, ancor_cooc))
```

<!-- #region slideshow={"slide_type": "fragment"} -->
Il y a **encore** un problème ?
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Oui
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Les débuggeurs

### Demo

Aller sur http://pythontutor.com/visualize.html et y coller le code de la factorielle buggué
<!-- #endregion -->

<!-- #region -->
```python
def factorial(n):
    if n == 0:
        return 1
    res = 1
    for i in range(1, n):
        res = i * res
    return res
    
factorial(9)
```
<!-- #endregion -->

On peut suivre l'exécution en détails \o/

<!-- #region slideshow={"slide_type": "subslide"} -->
On appelle ce genre d'interface un *debugger* : on peut suivre l'exécution du programme ligne par
ligne, en contrôlant les valeurs des variables et éventuellement en revenant en arrière pour
comprendre ce qui se passe
<!-- #endregion -->

C'est *très* pratique, mais la version de Python Tutor est (volontairement) assez limité. Pour notre
code en particulier ça va être compliqué à gérer.

<!-- #region slideshow={"slide_type": "subslide"} -->
### Pour les grand⋅e⋅s

On va débugger dans [Visual Studio Code](https://code.visualstudio.com/).

(On regarde le tableau, désolé pour celleux qui ne sont pas là)
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
### Pour les vraiment très grand⋅e⋅s

VSCode c'est bien, mais même ça a ses limites

- Quand le code prend toute la RAM
- Quand on débuggue à distance
- Quand on a pas d'interface graphique
- Quand on a une aversion viscérale à Microsoft
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Pour ça il existe une alternative directement incluse dans la bibliothèque standard :
[`pdb`](https://docs.python.org/3/library/pdb.html).

Pour le lancer, rien de plus simple (mais ça ne marche pas bien dans un notebook)
<!-- #endregion -->

<!-- #region -->
```bash
python -m pdb debugme.py
```
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
Là encore, on regarde le tableau. Pour référence future, tout est dans la doc mais les points
importants sont

- Les commandes (il suffit de taper la première lettre)
  - `l[ist]`: affiche les lignes autour de l'instruction courante
  - `ll[ist]`: affiche tout la fonction courante
  - `n[ext]`: passer à l'instruction suivante dans la fonction en cours
  - `s[tep]`: passer à l'instruction suivante y compris dans une autre fonction
  - `u[p]`: passer dans le contexte un niveau au dessus (l'instruction qui appelle la fonction
    courante)
  - `d[own]`: l'inverse de `u[p]`
- Commencer une ligne par un `!` fait exécuter une instruction, bien pratique pour lire le contenu
  des variables
- Dans n'importe quel progamme, une instruction `breakpoint()` stoppe l'exécution et vous donne une
  session `pdb`
  <!-- #endregion -->

<!-- #region slideshow={"slide_type": "subslide"} -->
C'est globalement un peu moins sympa qu'un débuggeur graphique, notamment pour voir en direct les
états des variables (mais il y a d'autres alternatives en console) mais ça marche vraiment bien.
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Exercice

Débugger et formatter `debugme.py`, envoyez-moi une pull request sur
<https://github.com/loicgrobol/web-interfaces>
<!-- #endregion -->
