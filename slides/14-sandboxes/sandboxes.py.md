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
      jupytext_version: 1.19.0
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- LTeX: language=fr -->

<!-- #region slideshow={"slide_type": "slide"} -->
Cours 14 : bacs à sable
=======================

**L. Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)
<!-- #endregion -->

Rappel : dans un notebook, une ligne qui commence par `!` est exécutée dans votre shell par défaut
(sur ma machine c'est `fish`, sur la vôtre probablement `bash`), une cellule qui commence par
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

```bash
alias
```

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
avez typiquement au moins `/bin`, `/usr/bin` et `/usr/local/sbin` dedans).

Comment ça marche ?

```bash
ls /usr/bin
```

Pour bash cette liste est stockée dans la variable `$PATH`

```bash
echo $PATH
```

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

- S'il existe un *builtin* ou une fonction qui s'appelle `machin`, on utilise ça.
- Sinon, on cherche dans chacun des dossiers de `$PATH`, dans l'ordre, s'il n'y a pas un fichier
  exécutable qui s'appelle `machin` dedans.

### Configurer son PATH

Comment changer votre `PATH`, par exemple pour y ajouter un dossier ? Ça dépend évidemment de votre
shell, mais pour bash, comme c'est juste une variable qui contient une chaîne de caractères, c'est
aussi simple que la troisième ligne dans la cellule suivante

```bash
echo $PATH
echo
export PATH="/mon/dossier:$PATH"
echo
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

Les programmes qui veulent modifier votre `PATH` (genre `conda`) ont tendance à aller modifier votre
`.bashrc` directement (ce qui est détestable), ou à vous demander de le modifier vous-même (ce qui
est ok), il contient donc souvent des trucs étranges que vous n'y avez pas mis.

En général, on ajoute à son `PATH`, un dossier comme `~/.local/bin`, où on a les droits d'écriture,
ce qui permet d'installer des programmes sans avoir à demander à l'admin système, et à séparer les
programme installés pour tous les utilisateurices de la machine et ceux à usage personnel

### Autres trucs à évoquer

arborscence standard (/etc, /bin, /lib etc.) et dossiers xdg. Liens dynamiques et `LD_LIBRARY_PATH`,
`rpath`.

## Python, installations et packages

### Python

Python est (en général) un langage *interprété*, c'est-à-dire que quand on exécute un programme en
Python, un programme, `python`, dit *interpréteur*, vient lire un *script* — un fichier texte qui
contient des instructions — et exécute ces instructions.

L'interpréteur est un programme comme un autre sur votre machine. En général vous le trouverez dans
`/usr/bin/python`, mais comme d'habitude, on peut utiliser `which`.

```bash
which python
python --version
```

(On reparle de ce résultat dans une seconde si ce n'est pas `/usr/bin/python`)

En général, vous utilisez CPython, qui est écrit en langage C, mais il y en a d'autres versions !
Notablement Jython (écrit en Java), RustPython (en Rust) et PyPy (écrit lui-même en Python, promis
ça a du sens).


En simplifiant : tout ce qui permet d'exécuter des programmes en Python est dans ce fichier
`/usr/bin/python`.

### Modules

Sauf qu'on sait que c'est pas vrai :

```python
import pathlib

pathlib.__file__
```

Pour ne pas surcharger l'exécutable `python` et éviter de ralentir l'exécution avec des
fonctionnalités qui ne servent pas à tous les scripts, une bonne partie du langage est en fait
distribuée dans les *modules* de la bibliothèque standard. Ces modules correspondent à des fichiers
Python (typiquement dans `/usr/lib/python3.xx/` ou `/usr/lib/python3.xx/site-packages`) et à des
bibliothèques compilées (typiquement dans `/usr/lib/python3.xx/lib-dynload`).

Historiquement, pour ajouter des modules à Python et les rendre accessibles à tous les scripts, on
pouvait donc simplement les copier dans `site-packages`. Ça peut être fait à la main, ou via des
packages systèmes, par exemple
[`python3-requests`](https://packages.ubuntu.com/oracular/python3-requests) dans Ubuntu.

Faire un package système, c'est lourd, et copier à la main, c'est sujet à plein d'erreurs. On a donc
développé des outils pour aider à gérer `site-packages` ont été développés :

- `distutils` (Python 1.6, 2000), un module de la bibliothèque standard pour créer des scripts
  d'installation avec un peu de métadonnées, en particulier des *versions*
- Des formats de métadonnées dans les PEP [241](https://peps.python.org/pep-0241/),
  [314](https://peps.python.org/pep-0314/), [345](https://peps.python.org/pep-0345/),
  [566](https://peps.python.org/pep-0566/), [643](https://peps.python.org/pep-0643/)…
- [PyPI](https://pypi.org/), le cheeseshop, un dépôt de packages accessibles programmatiquement.
- Setuptools, un successeur à distutils qui introduit le format de distribution source Egg.
- Le format de distribution [*standardisé*](https://peps.python.org/pep-0427/) Wheel, qui peut
  contenir des fichiers compilés (« *binaries* »).
- **Pip**, un installateur de package reposant sur Setuptools et interfaçant avec PyPI.

(voir [The hitchhiker's guide to Python
packaging](https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/history.html) pour un
historique (obsolète))

Du point de vue utilisateurice, l'objectif final de tout ça c'est une interface qui permet de faire
`pip install nomdupackage`, qu'un package soit localisé dans un index (en général PyPI), téléchargé,
et installé dans `site-packages`, avec gestion des versions et des dépendances.

Tout va pour le mieux dans le meilleur des mondes, avec quelques bizarreries (genre Debian qui
remplace `site-packages` par `dist-packages`) mais c'est OK.

Quels problèmes vous voyez apparaître ?

### Permissions

Évidemment un des problèmes d'avoir les packages installés dans `/usr/lib/…`, c'est que ce sont des
fichiers qui ne sont pas en accessible en écriture aux utilisateurices dans Linux. Évidemment si
vous avez les droits pour ça, vous pouvez vous mettre en mode superuser avec `sudo` et le faire
quand même, mais ce n'est pas idéal (en particulier parce que ça risque de perturber votre OS, qui
gère déjà ses propres packages). Donc on retient : jamais, jamais, jamais on écrit ~~`sudo pip`~~.

Pour ça, comme pour `PATH`, Python va lire dans une variable d'environnement, `PYTHONPATH`, une
liste de dossiers où il ira chercher des modules. Son contenu est accessible dans `sys.path` :

```python
import sys
sys.path
```

Cette variable est modifiable au même titre que `PATH` pour y ajouter des dossiers à la convenance
des utilisateurices.


En surplus, pour des raisons de simplicité, Python va aussi chercher des modules dans un dossier
d'installation locale (s'il existe), dans `~/.local/lib/python3.xx/…`. Jusqu'à récemment,
l'installation dans cet espace pouvait être demandé à Pip avec l'option `--user`.


Le deuxième problème, plus difficile à régler, c'est que plusieurs projets peuvent avoir des
dépendances incompatibles. Par exemple si mon projet `A` dépend de PyTorch 1, et `B` dépend de
Pytorch 2. Dans ces projets, il peut aussi y avoir le système même : Ubuntu, Manjaro… dépendent pour
leur fonctionnement de packages Python, ça signifie a priori qu'il ne serait pas possible d'utiliser
des versions de packages différentes de celles nécessaire au système pour des projets personnels, ce
qui est, là encore, très peu pratique.

## Environnements

Pour régler ce deuxième problème, on peut manipuler complètement `PYTHONPATH` et éventuellement
`PYTHONHOME` (qui donne le chemin de la bibliothèque standard), en construisant un `site-packages`
parallèle. C'est un peu lourd à gérer à la main, et des outils ont donc été construit pour aider à
ça : workingenv, puis surtout [virtualenv](https://pypi.org/project/virtualenv).

Ce procédé a été simplifié et standardisé par la [PEP 405](https://peps.python.org/pep-0405/) (qu'il
vaut le coup de lire). Concrètement, quand `python` est invoqué, il cherche un fichier `pyvenv.cfg`
qui lui est adjacent ou dans le dossier parent. S'il en trouve un, il sait qu'il est dans une
installation isolée, et ne va chercher les modules et la bibliothèque standard que dans celle-ci.


Un environnement a en général cette structure

```text
/
├── bin
│   ├── python
│   └── …
├── etc
│   └── …
├── include
│   └── site
├── lib
│   └── python3.xx
│       └── site-packages
├── lib64 -> lib
├── pyvenv.cfg
└── share
    └── …
```

Elle fait mirroir à la structure UNIX standard, et contient des copies (ou des liens symboliques)
d'une installation Python autonome, y compris les fichiers des packages (données dans `share`,
programmes dans `bin`…), etc. `pyvenv.cfg` contient aussi quelques options de configuration de
l'environnement.

Si on exécute le programme `{virtenv}/bin/python`, où `{virtenv}` est le chemin vers l'environnement
virtuel, cette instance de Python va donc détecter automatiquement qu'il est dans cet environnement,
et utiliser cette installation en conséquence.


Notez que ça permet non seulement d'avoir plusieurs `site-packages` isolés, mais aussi d'utiliser
facilement plusieurs versions de Python lui-même, isolées de l'installation système. Ainsi certains
de mes environnements à l'heure où j'écris ces lignes contiennent un Python 3.13, et d'autres sont
restés en 3.12.


Après le succès de `virtualenv`, d'autres alternatives sont apparues pour créer et gérer des
environnements virtuels : `venv` (qui est juste virtualenv redistribué dans la bibliothèque standard
de Python, sauf sous Debian et variantes qui ne peuvent rien faire comme tout le monde), Poetry,
PipEnv, uv, virtualfish (pour fish), vox et uvox (pour Xonsh)…

### Activer un environnement

On peut donc utiliser un Python isolé en exécutant directement `{virtenv}/bin/python`, mais c'est un
peu désagréable, ce serait mieux de pouvoir décider « dans cette session, j'utilise l'environnement
machin » et qu'ensuite, simplement appeler `python` nous donne l'environnement choisi.

Une idée de comment faire ?

<!-- #region -->
En modifiant `PATH` ! C'est ce que font les *scripts d'activation*, qui sont facultatifs (de fait la
spécification des environnements virtuels n'impose que le fichier `pyvenv.cfg`) que la plupart des
gestionnaires d'environnements mettent dans `{virtenv}/bin/`. Par exemple voici un bout de
`{virtenv}/bin/activate`, qu'on peut ajouter à une session bash avec `source {virtenv}/bin/activate`
pour modifier `PATH` :

```bash
[…]

VIRTUAL_ENV='/home/lgrobol/.virtualenvs/cours-web'
if ([ "$OSTYPE" = "cygwin" ] || [ "$OSTYPE" = "msys" ]) && $(command -v cygpath &> /dev/null) ; then
    VIRTUAL_ENV=$(cygpath -u "$VIRTUAL_ENV")
fi
export VIRTUAL_ENV

_OLD_VIRTUAL_PATH="$PATH"
PATH="$VIRTUAL_ENV/bin:$PATH"
export PATH

[…]
```
<!-- #endregion -->

En plus de modifier `PATH` (vous voyez où ?), il définit un certain nombre de variables comme
`VIRTUAL_ENV`, relativement standard, qui permettent aux programmes de déterminer qu'ils ont été
invoqués dans un environnement virtuel. Il définit aussi la fonction `deactivate`, qui fait de son
mieux pour remettre le shell dans l'état où il était avant l'activation.

Il y a aussi des `activate.fish`, `activate.csh`…


Notez que ce n'est pas un mécanisme très robuste, même s'il est pratique. Parmi les défauts
notables, on ne peut pas enchâsser les activations (il faut désactiver un environnement avant
d'activer le suivant), certains programmes comme Pip ne détectent pas bien l'environnement en toutes
circonstances (il vaut donc mieux l'appeler avec `python -m pip` pour être sûr⋅e que c'est bien le
Pip de l'environnement virtuel qu'on utilise et pas un autre), etc.


En résumé, pour utiliser une installation indépendante de Python :

- On crée un environnement virtuel
- Quand on veut travailler dedans, on peut
    - Appeler Python via son chemin complet
    - Activer l'environnement dans son shell `source /mon/env/virt/bin/activate`… et utiliser
      simplement `python` 
- Pour installer des paquets, préférer `python -m pip` à juste `pip`
- Quand on a fini, on `deactivate` (ou on ferme le terminal et on en rouvre un autre au besoin…)


### Conventions

Les environnements virtuels, ce sont donc des dossiers sur votre machine, sans plus de contrainte.
En général on les place

- Soit dans le dossier de votre projet, dans un dossier `.venv`
- Soit dans votre home, dans `~/.virtualenvs/{nom}` (convention de virtualenvwrapper)

La plupart des outils (genre vscode) vont aller les chercher dans ces endroits là, je vous
recommande donc d'utiliser ça, sauf si vous avez une bonne raison de faire autrement.

<!-- #region -->
## D'autres installations

### uv

[uv](https://docs.astral.sh/uv/), développé par Astral à qui on doit aussi Ruff est une alternative
à Pip et VirtualEnv (et un successeur/remplaçant de [rye](https://rye.astral.sh/)). Écrit en Rust,
très très optimisé pour la rapidité et l'économie d'espace disque, il permet de :

- Installer et gérer plusieurs versions de Python
- Créer et gérer des environnements virtuels
- Gérer des packages (mais seulement dans des environnements)

En général, uv respecte bien les standards et s'assure de vous empêcher de vous tirer des balles
dans les pieds (c'est pour ça qu'il ne marche que dans des environnements par exemple).

Vous l'aurez compris, je vous encourage très fort à l'utiliser. Allez voir leur doc pour l'installer, puis

- `uv venv` pour créer des environnements, qui s'activent comme d'habitude.
    - Par défaut il utilise la version de Python de votre système, mais vous pouvez changer ça avec
      l'option `-p`, genre `uv venv … -p 3.12`.
- `uv pip` qui propose un clone de interface de Pip
- `uv tool` permet d'installer des packages Python comme outils, dans des environnements dédiés.
  Essayez par exemple `uv tool install cowsay`.
<!-- #endregion -->

<!-- #region -->
### Pyenv

Un peu rendu obsolète par uv

### [Pixi](https://pixi.sh)

Encore un peu neuf. Et en priorité base sur Conda (qui est bof).
<!-- #endregion -->

## Et Conda ?

Non.

Enfin bon.

Conda c'est un écosystème complètement parallèle, qui offre les mêmes fonctionnalités que
Pip+virtualenv+PyPI, avec comme unique avantage que leur dépôt de paquet contient aussi des
bibliothèques non-Python (comme CUDA), même si c'est aussi des choses qui commencent à arriver sur
PyPI. Ça peut rester utile dans certains cas, notamment si vous écrivez beaucoup d'extensions en
C/C++/Rust, etc. Mais c'est absolument dispensable.

À part ça

- Conda ne suit pas de façon consistante les standards de packaging
- Les packages sont (et doivent) construits à part de ceux de l'écosystème standard et ne sont en
  général pas compatible
- Même tarif pour les versions de Python
- Tout l'écosystème dépend complètement d'Anaconda Inc et n'existe pas vraiment s'ils disparaissent.
- Conda modifie sauvagement votre bashrc sans demander la permission et ça c'est impardonnable.

## Conteneurs

Docker et les autres

## Machines virtuelles

Juste dire ce que c'est

Exos: tout péter, puis tout restorer
