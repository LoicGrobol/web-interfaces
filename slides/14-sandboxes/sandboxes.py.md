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
Cours 14 : bacs à sable
=======================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)
<!-- #endregion -->

Rappel : dans un notebook, une ligne qui commence par `!` est exécutée dans votre shell par défaut
(sur ma machinee c'est `fish`, sur la vôtre probablement `bash`), une cellule qui commence par
`%%bash` est exécutée comme un script bash indépendant (les cellules bash n'interagissent pas entre
elles).

## D'où viennent les commandes ?

### Dans un terminal


Quand vous interagissez avec votre machine via un terminal, vous :

- Saisissez des instructions :

```python
!ls
```

Qui peuvent avoir des arguments :

```python
!echo "spam"
```

Et qu'on peut combiner

```bash
help | head -n 16
```

- Utilisez des structures de contrôle :

```bash
for e in "a" "b" "c"; do echo $e; done;
```

```bash
if [ $(pwd | grep home) ]; then echo "yea"; else echo "nope"; fi;
```

Toutes ces choses ne sont pas les mêmes :

- `ls` est un programme, il est contenu dans un fichier autonome sur votre machine sous forme
  d'instruction en langage machine :

```python
!xxd /usr/bin/ls | head -n 16
```

Et je peux l'appeler directement :

```bash
/usr/bin/ls
```

La règle est la suivante : si le début d'une instruction en bash est le chemin vers un fichier
exécutable (concrètement un fichier que vous avez la permission d'exécuter), bash va essayer de
l'exécuter.


- `help` est un *builtin* de bash


Comment je peux savoir ça ? Avec le programme `type` :

```bash
type -a help
```

```bash
type -a ls
```

Ou avec `which`

```bash
which ls
```

```bash
which help
```

Des fois il y a les deux

```bash
type -a echo
```

Les structures de contrôle, elles sont des *keywords*

```bash
type -a if
```

Quelles sont les commandes utilisées dans la cellule suivante ?

```bash
ls
echo "spam"
if [ $(pwd | grep home) ]; then echo "yea"; else echo "nope"; fi;
for e in "a" "b" "c"; do echo $e; done;
```

```bash
which [
```

Autres trucs qui existent dans bash (et en fait dans tous les shells) : fonctions et alias.

### Ok mais où

Pour les *builtins* et les *keywords*, la question de comment bash sait quoi en faire ne se pose pas
trop : c'est codé directement dans bash.

Par contre, pour `ls`, par exemple, c'est plus compliqué : comment quand je saisis `ls`, bash sait
qu'il faut aller chercher `/usr/bin/ls` ?

On pourrait se dire que bash a un registre des commandes qui existent sur le système et qu'il va les
chercher là. C'est possible mais pas très pratique : ça veut dire que quand on veut installer de
nouveau programmes, il faut savoir que bash est installé sur la machine, lui dire qu'on a ajouté une
nouvelle commande et lui dire où, et répéter ça pour tous les shells de la machine.

Pas top.


À la place, la solution qui est adoptée sur tous (à peu près) les OS, c'est d'avoir une liste de
dossier qui vont contenir des programmes. Certains sont conventionnels (par exemple sur Linux, vous
avez typiquement au moins `/bin`, `/usr/bin` et `/usr/sbin` dedans).

Comment ça marche ?

Sans rentrer dans trop de détails : `$PATH` dans bash combine plusieurs

- La valeur de la variable d'environnement `PATH`, qui est passé à bash par le programme parent
- Des modifications apportées par des *scripts d'initialisation* (on en parle dans un instant)

Les *variables d'environnement* sont des valeurs couple clé/valeur de chaînes de caractères qui sont
passées au programme via l'appel système qui l'a invoqué. Vous pouvez voir ce qui a été passé à un
programme dans le pseudo-fichier `/proc/{pid}/environ`, où `{pid}` est l'identifiant numérique du
programme. Quand vous exécutez un programme via bash, il hérite de l'environnement de cette instance
de bash, que vous pouvez voir avec le programme `env` :

```bash
env
```

Précisément, `$PATH` ressemble à ça

```bash
echo $PATH
```

C'est-à-dire une chaine de caractère qui encode une liste de chemins absolus vers des dossiers,
séparés par des `:`. Certains shells comme fish ou Xonsh le ré-encodent indépendamment comme une
vraie liste dans leurs structures de données propres.


Quand vous saisissez une instruction comme `machin` dans bash, son protocole est donc

- S'il existe un *builtin* qui s'appelle `machin`, on utilise ça.
- Sinon, on cherche dans chacun des dossiers de `$PATH`, dans l'ordre, s'il n'y a pas un fichier
  exécutable qui s'appelle `machin` dedans.

### Configurer son PATH

Comment changer votre `PATH`, par exemple pour y ajouter un dossier ? Ça dépend évidemment de votre
shell, mais pour bash, comme c'est juste une variable qui contient une chaîne de caractères, c'est
aussi simple que la deuxième ligne dans la cellule suivante

```bash
echo $PATH
export PATH="/mon/dossier:$PATH"
echo $PATH
```

`export` étant le *builtin* de bash qui permet de modifier les variables d'environnement. En
conséquence, cette instance de bash et tous ses processus enfants invoqués à la suite auront ce
`PATH` modifié et pourront donc trouver les programmes dans ce dossier.


Bash (au contraire de fish par exemple) n'a pas de moyen de rendre cette modification pérenne, elle
ne concerne que l'instance en cours. Pour ajouter durablement un dossier au `PATH`, il faut donc que
ce `export` soit refait à chaque fois. Soit manuellement (bof), soit en modifiant un fichier
`.profile` (`~/.profile`, `/etc/profile`, qui sont exécutés par le shell de connexion dont tous les
programmes de votre session héritent, y compris ceux qui sont lancés via une interface graphique) ;
soit un `.bashrc` (typiquement `~/.bashrc`), qui est exécuté par chaque instance de bash que vous
lancez vous. Dans le doute `~/.profile` est la meilleure solution.

```bash

cat ~/.bashrc
```

Les programmes qui veulent modifier votre `PATH` (genre `©onda`) ont tendance à aller modifier votre
`.bashrc` directement (ce qui est détestable), ou à vous demander de le modifier vous-même (ce qui
est ok), il contient donc souvent des trucs étranges que vous n'y avez pas mis.

### Autres trucs à évoquer

Liens dynamiques et `LD_LIBRARY_PATH`, `rpath`.

## Python, installations et packages


site packages, installation à la mano, installation avec un gestionnaire de paquets système,
installation avec pip, user obsolè

### Python

Python est (en général) un langage *interprété*, c'est-à-dire que quand on exécute un programme en
Python, un programme, `python`, dit *interpréteur*, vient lire un *cript* — un fichier texte qui
contient des instructions — et exécute ces instructions.

L'interpréteur est un programme comme un autre sur votre machine. En général vous le trouverez dans
`/usr/bin/python`, mais comme d'habitude, on peut utiliser `which`.

```bash
which python
python --version
```

(On reparle de ce résultat dans une seconde si ce n'est pas `/usr/bin/python`)

En général, vous utilisez CPython, qui est écrit en lagage C, mais il y en a d'autres versions !
Notablement Jython (écrit en Java), RustPython (en Rust) et PyPy (écrit lui-même en Python, promis
ça a du sens).


En simplifiant : tout ce qui permet d'exécuter des programmes en Python est dans ce fichier `/usr/bin/python`.

### Modules

Sauf que on sait que c'est pas vrai :

```python
import pathlib

pathlib.__file__
```

Pour ne pas surcharger l'exécutable `python` et éviter de ralentir l'exécution avec des fonctionnalités
qui ne servent pas à tous les scripts, une bonne partie du langage est en fait distribuée dans les
*modules* de la bibliothèque standard. Ces modules correspondent à des fichiers Python (typiquement
dans `/usr/lib/python3.xx/site-packages`) et à des bibliothèques compilées (typiquement dans
`/usr/lib/python3.xx/lib-dynload`).




## Environnements virtuels

historique, fonctionnement

virtualenv, venv,

## D'autres installations

pyenv et uv

## Conteneurs

Docker et les autres

## Machines virtuelles

Juste dire ce que c'est

Exos: tout péter, puis tout restorer
