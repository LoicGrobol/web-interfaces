---
title: Interfaces web pour le TAL — M2 PluriTAL 2026
layout: default
---


<!-- LTeX: language=fr -->

## News

- **2025-11-24** Premier cours du semestre le 02/12/2025.

## Infos pratiques

- **Quoi** « Interfaces web pour le TAL »
- **Où** Salle ???, bâtiment de la formation continue.
- **Quand** 8 séances, les mardi de 09:30 à 12:30, du 24/11/2025 au ???/2026
- **Contact** L. Grobol [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

## Liens utiles

- Prendre rendez-vous pour des *office hours* en visio :
  [mon calendrier](https://calendar.app.google/N9oW2c9BzhXsWrrv9)

## Séances

Les liens dans chaque séance vous permettent de télécharger les fichiers `.ipynb` à utiliser (et
données additionnelles éventuelles). Attention : pour les utiliser en local, il faudra installer les
packages du `requirements.txt` (dans un environnement virtuel). Si vous ne savez pas comment faire,
allez voir [« Utilisation en local »](#utilisation-en-local)

### 2025-12-02 — Internet et programmation orientée objet

- {% notebook_badges slides/01-internet/internet.py.md %} [Notebook
  internet]({{site.url}}{{site.baseurl}}/slides/01-internet/internet.py.ipynb)
  - [Solutions exercices cURL]({{site.url}}{{site.baseurl}}/slides/01-internet/curl.sh)
- {% notebook_badges slides/02-OOP/oop.py.md %} [Notebook
  OOP]({{site.url}}{{site.baseurl}}/slides/02-OOP/oop.py.ipynb)
  - [Treebank GSD-fr train]({{site.url}}{{site.baseurl}}/slides/02-OOP/data/fr_gsd-ud-train.conllu)
  - Solutions :
    - [Script v1]({{site.url}}{{site.baseurl}}/slides/02-OOP/correction_conllu_v1.py)
    - [Script v2]({{site.url}}{{site.baseurl}}/slides/02-OOP/correction_conllu_v2.py)

### 2025-12-08 — Modules et HTTPX

- {% notebook_badges slides/04-modules/modules.py.md %} [Notebook
  Modules]({{site.url}}{{site.baseurl}}/slides/04-modules/modules.py.ipynb)

- {% notebook_badges slides/03-httpx/httpx.py.md %} [Notebook
  HTTPX]({{site.url}}{{site.baseurl}}/slides/03-httpx/httpx.py.ipynb)
  
  Solutions :

  - [Requêtes]({{site.url}}{{site.baseurl}}/slides/03-httpx/solutions.py)
  - [Script sans rien]({{site.url}}{{site.baseurl}}/slides/03-httpx/requrl_base.py)
  - [Script avec `click`]({{site.url}}{{site.baseurl}}/slides/03-httpx/requrl_click.py)
  - [Script avec `argparse`]({{site.url}}{{site.baseurl}}/slides/03-httpx/requrl_argparse.py)

### 2025-12-15 — APIs REST en mode client

- {% notebook_badges slides/05-REST/rest.py.md %} [Notebook
  REST]({{site.url}}{{site.baseurl}}/slides/05-REST/rest.py.ipynb)

Vos solutions pour les exercices du notebook REST sont à envoyer dans un zip à
<lgrobol@parisnanterre.fr> avant le 29/01. L'objet du message devra être `[Web 2026] TP REST` et le
nom de fichier devra être de la forme `prénom_nom-établissment.zip`, `établissement` étant
`Nanterre`, `P3` ou `Inalco` et vos prénoms et noms doivent être présents dans le corps du message.
Ce n'est pas grave si vous n'arrivez pas à finir le dernier exercice, mais essayez !

### 2026-01-12 — Fonctions avancées et FastAPI

- {% notebook_badges slides/06-functions++/functions++.py.md %} [Notebook
  décorateurs]({{site.url}}{{site.baseurl}}/slides/06-functions++/functions++.py.ipynb)
  - [Liste de Swadesh pour les langues
    austronésiennes]({{site.url}}/{{site.baseurl}}/slides/07-fastapi/data/austronesian_swadesh.csv)
  - {% notebook_badges slides/06-decorators/solutions.py.md %}
    [Solutions]({{site.url}}{{site.baseurl}}/slides/06-functions++/solutions.py.ipynb)
- {% notebook_badges slides/07-fastapi/fastapi.py.md %} [Notebook
  FastAPI]({{site.url}}{{site.baseurl}}/slides/07-fastapi/fastapi.py.ipynb)
  - [Exemples](https://github.com/{{site.repository}}/tree/main/slides/07-fastapi/examples).
  - {% notebook_badges slides/07-fastapi/solutions.py.md %}
    [Solutions]({{site.url}}{{site.baseurl}}/slides/07-fastapi/solutions.py.ipynb)

### 2026-01-20 — HTML

- {% notebook_badges slides/07-fastapi/fastapi.py.md %} [Notebook
  FastAPI]({{site.url}}{{site.baseurl}}/slides/07-fastapi/fastapi.py.ipynb)
  - [Exemples](https://github.com/{{site.repository}}/tree/main/slides/07-fastapi/examples).
  - {% notebook_badges slides/07-fastapi/solutions.py.md %}
    [Solutions]({{site.url}}{{site.baseurl}}/slides/07-fastapi/solutions.py.ipynb)
- {% notebook_badges slides/08-html/html-slides.py.md %} [Slides
  HTML]({{site.url}}{{site.baseurl}}/slides/08-html/html-slides.py.ipynb)
  - [Exemples](https://github.com/{{site.repository}}/tree/main/slides/08-html/examples)
  - {% notebook_badges slides/08-html/solutions.py.md %}
    [Solutions]({{site.url}}{{site.baseurl}}/slides/08-html/solutions.py.ipynb)

## Utilisation en local

### Environnements virtuels et packages

Je cite le [Crash course Python](slides/01-tools/python_crash_course.py.ipynb):

- Les environnements virtuels sont des installations isolées de Python. Ils vous permettent d'avoir
  des versions indépendantes de Python et des packages que vous installez
  - Gérez vos environnements et vos packages avec [uv](https://docs.astral.sh/uv/). Installez-le,
    lisez la doc.
  - Pour créer un environnement virtuel : `uv venv /chemin/vers/…`
  - La convention, c'est `uv venv .venv`, ce qui créée un dossier (caché par défaut sous Linux et
    Mac OS car son nom commence par `.`) : `.venv` dans le dossier courant (habituellement le
    dossier principal de votre projet). Donc faites ça.
  - Il est **obligatoire** de travailler dans un environnement virtuel. L'idéal est d'en avoir un
    par cours, un par projet, etc. - uv est assez précautionneux avec l'espace disque, il y a donc
    assez peu de désavantage à avoir beaucoup d'environnements virtuels.
  - Un environnement virtuel doit être **activé** avant de s'en servir. Concrètement ça remplace la
    commande `python` de votre système par celle de l'environnement. - Dans Bash par exemple, ça se
    fait avec `source .venv/bin/activate` (en remplaçant par le chemin de l'environnement s'il est
      différent) - `deactivate` pour le désactiver et rétablir votre commande `python`. À faire
    avant d'en activer un autre.
- On installe des packages avec `uv pip` ou `python -m pip` (mais plutôt `uv pip`, et jamais juste
  `pip`).
  - `uv pip install numpy` pour installer Numpy.
  - Si vous avez un fichier avec un nom de package par ligne (par exemple le
    [`requirements.txt`](https://github.com/LoicGrobol/web-interfaces/blob/main/requirements.txt) du
    cours) : `uv pip install -U -r requirements.txt`
  - Le flag `-U` ou `--upgrade` sert à mettre à jour les packages si possible : `uv pip install -U
    numpy` etc.
- Je répète : on installe uniquement dans un environnement virtuel, on garde ses environnements bien
  séparés (un par cours, pas un pour tout le M2).
  - Dans un projet, on note dans un `requirements.txt` (ou `.lst`) les packages dont le projet a
    besoin pour fonctionner.
  - Les environnements doivent être légers : ça ne doit pas être un problème de les effacer, de les
    recréer… Si vous ne savez pas recréer un environnement que vous auriez perdu, c'est qu'il y a un
    problème dans votre façon de les gérer.
- Si vous voulez en savoir plus, **et je recommande très fortement de vouloir en savoir plus, c'est
  vital de connaître ses outils de travail**, il faut : *lire les documentations de **tous** les
  outils et **toutes** les commandes que vous utilisez*.

Maintenant à vous de jouer :

- Installez uv
- Créez un dossier pour ce cours
- Dans ce dossier, créez un environnement virtuel nommé `.venv`
- Activez-le
- Téléchargez le
  [`requirements.txt`](https://github.com/LoicGrobol/web-interfaces/blob/main/requirements.txt)
  et installez les packages qu'il liste

### Notebooks Jupyter

Si vous avez une installation propre (par exemple en suivant les étapes précédentes), vous pouvez
facilement ouvrir les notebooks du cours :

- Téléchargez le notebook du [Crash course
  Python](https://loicgrobol.github.io/apprentissage-artificiel/slides/01-tools/python_crash_course.py.ipynb)
  et mettez-le dans le dossier que vous utilisez pour ce cours.
- Dans un terminal (avec votre environnement virtuel activé) lancez jupyter avec `jupyter notebook
  python_crash_course.py.ipynb`.
- Votre navigateur devrait s'ouvrir directement sur le notebook. Si ça ne marche pas, le terminal
  vous donne dans tous les cas un lien à suivre.

Alternativement, des IDE comme vscode permettent d'ouvrir directement les fichiers ipynb. Pensez à
lui préciser que le kernel à utiliser est celui de votre environnement virtuel s'il ne le trouve pas
tout seul.

### Utilisation avancée

Vous pouvez aussi (mais je ne le recommande pas forcément car ce sera plus compliqué pour vous de le
maintenir à jour) cloner [le dépôt du
cours](https://github.com/loicgrobol/apprentissage-artificiel). Tous les supports y sont, sous forme
de fichiers Markdown assez standards, qui devraient se visualiser correctement sur la plupart des
plateformes. Pour les utiliser comme des notebooks, il vous faudra utiliser l'extension
[Jupytext](https://github.com/mwouts/jupytext) (qui est dans le `requirements.txt`). C'est entre
autres une façon d'avoir un historique git propre.

## Ressources

Il y a beaucoup, beaucoup de ressources disponibles pour apprendre Python. Ce qui suit n'est qu'une
sélection.

## Livres

- *How to think like a computer scientist*, by Jeffrey Elkner, Allen B. Downey, and Chris Meyers.
Vous pouvez l'acheter. Vous pouvez aussi le lire
[ici](http://openbookproject.net/thinkcs/python/english3e/)
- *Dive into Python*, by Mark Pilgrim. [Ici](http://www.diveintopython3.net/) Un peu ancien, mais
toujours pas mal. Vous pouvez le lire en ligne ou télécharger le pdf.
- *Learning Python*, by Mark Lutz.
- *Beginning Python*, by Magnus Lie Hetland.
- *Python Algorithms: Mastering Basic Algorithms* in the Python Language, by Magnus Lie Hetland.
- *Programmation Efficace. Les 128 Algorithmes Qu'Il Faut Avoir Compris et Codés en Python au Cours
  de sa Vie*, by Christoph Dürr and Jill-Jênn Vie. Si le cours vous paraît trop facile. Le code
  Python est clair, les difficultés sont commentées.

## Web

Il vous est vivement conseillé d'utiliser un (ou plus) des sites et tutoriels ci-dessous.

- [Real Python](https://realpython.com), des cours et des tutoriels souvent de très bonne qualité et
  pour tous niveaux.
- [Coding Game](https://www.codingame.com/home). Vous le retrouverez dans les exercices
  hebdomadaires.
- [Code Academy](https://www.codecademy.com/fr/learn/python)
- [newcoder.io](http://newcoder.io/). Des projets commentés, commencer par 'Data Visualization'
- [Google's Python Class](https://developers.google.com/edu/python/). Guido a travaillé chez eux.
  Pas [ce
  Guido](http://vignette2.wikia.nocookie.net/pixar/images/1/10/Guido.png/revision/latest?cb=20140314012724),
  [celui-là](https://en.wikipedia.org/wiki/Guido_van_Rossum#/media/File:Guido_van_Rossum_OSCON_2006.jpg)
- [Mooc Python](https://www.fun-mooc.fr/courses/inria/41001S03/session03/about#). Un mooc de
  l'INRIA, carré.
- [Code combat](https://codecombat.com/)

## Licences

[![CC BY Licence badge](https://i.creativecommons.org/l/by/4.0/88x31.png)](http://creativecommons.org/licenses/by/4.0/)

Copyright © 2025 L. Grobol [\<lgrobol@parisnanterre.fr\>](mailto:lgrobol@parisnanterre.fr)

Sauf indication contraire, les fichiers présents dans ce dépôt sont distribués selon les termes de
la licence [Creative Commons Attribution 4.0
International](https://creativecommons.org/licenses/by/4.0/). Voir [le README](README.md#Licences)
pour plus de détails.

Un résumé simplifié de cette licence est disponible à
<https://creativecommons.org/licenses/by/4.0/>.

Le texte intégral de cette licence est disponible à
<https://creativecommons.org/licenses/by/4.0/legalcode>
