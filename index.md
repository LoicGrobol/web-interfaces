---
title: Interfaces web pour le TAL — M2 PluriTAL 2025
layout: default
---


<!-- LTeX: language=fr -->

## News

- **2024-12-17** Les [consignes pour les projets]({{site.url}}{{site.baseurl}}/projects) sont en
  ligne.
- **2024-11-19** Premier cours du semestre le 28/11/2023.

## Infos pratiques

- **Quoi** « Interfaces web pour le TAL »
- **Où** Salle 408, bâtiment de la formation continue.
- **Quand** 8 séances, les mardi de 13:30 à 16:30, du 28/11/22 au 31/01/24
- **Contact** L. Grobol [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

## Liens utiles

- Prendre rendez-vous pour des *office hours* en visio :
  [mon calendrier](https://calendar.app.google/N9oW2c9BzhXsWrrv9)
- Lien Binder de secours :
  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/LoicGrobol/web-interfaces/main)

## Séances

Tous les supports sont sur [github](https://github.com/loicgrobol/web-interfaces), voir
[Utilisation en local](#utilisation-en-local) pour les utiliser sur votre machine comme des
notebooks. À défaut, ce sont des fichiers Markdown assez standards, qui devraient se visualiser
correctement sur la plupart des plateformes (mais ne seront pas dynamiques).

Les slides et les notebooks ci-dessous ont tous des liens Binder pour une utilisation interactive
sans rien installer. Les slides ont aussi des liens vers une version HTML statique utile si Binder
est indisponible.

### 2024-11-19 — Internet et programmation orientée objet

- {% notebook_badges slides/01-internet/internet.py.md %} [Notebook
  internet]({{site.url}}{{site.baseurl}}/slides/01-internet/internet.py.ipynb)
  - [Solutions exercices cURL]({{site.url}}{{site.baseurl}}/slides/01-internet/curl.sh)
- {% notebook_badges slides/02-OOP/oop.py.md %} [Notebook
  OOP]({{site.url}}{{site.baseurl}}/slides/02-OOP/oop.py.ipynb)
  - [Treebank GSD-fr train]({{site.url}}{{site.baseurl}}/slides/02-OOP/data/fr_gsd-ud-train.conllu)
  - Solutions :
    - [Script v1]({{site.url}}{{site.baseurl}}/slides/02-OOP/correction_conllu_v1.py)
    - [Script v2]({{site.url}}{{site.baseurl}}/slides/02-OOP/correction_conllu_v2.py)

### 2024-11-26 — Modules et HTTPX

- {% notebook_badges slides/04-modules/modules.py.md %} [Notebook
  Modules]({{site.url}}{{site.baseurl}}/slides/04-modules/modules.py.ipynb)

- {% notebook_badges slides/03-httpx/httpx.py.md %} [Notebook
  HTTPX]({{site.url}}{{site.baseurl}}/slides/03-httpx/httpx.py.ipynb)
  
  Solutions :

  - [Requêtes]({{site.url}}{{site.baseurl}}/slides/03-httpx/solutions.py)
  - [Script sans rien]({{site.url}}{{site.baseurl}}/slides/03-httpx/requrl_base.py)
  - [Script avec `click`]({{site.url}}{{site.baseurl}}/slides/03-httpx/requrl_click.py)
  - [Script avec `argparse`]({{site.url}}{{site.baseurl}}/slides/03-httpx/requrl_argparse.py)

### 2023-12-19 — APIs REST en mode client

- {% notebook_badges slides/05-REST/rest.py.md %} [Notebook
  REST]({{site.url}}{{site.baseurl}}/slides/05-REST/rest.py.ipynb)

Vos solutions pour les exercices du notebook REST sont à envoyer dans un zip à
<lgrobol@parisnanterre.fr> avant le 29/01. L'objet du message devra être `[Web 2024] TP REST` et le
nom de fichier devra être de la forme `prénom_nom-établissment.zip`, `établissement` étant
`Nanterre`, `P3` ou `Inalco` et vos prénoms et noms doivent être présents dans le corps du message.

### 2024-12-10 — Fonctions avancées et FastAPI

- {% notebook_badges slides/06-functions++/functions++.py.md %} [Notebook
  décorateurs]({{site.url}}{{site.baseurl}}/slides/06-functions++/functions++.py.ipynb)
  - {% notebook_badges slides/06-decorators/solutions.py.md %}
    [Solutions]({{site.url}}{{site.baseurl}}/slides/06-functions++/solutions.py.ipynb)
- {% notebook_badges slides/07-fastapi/fastapi.py.md %} [Notebook
  FastAPI]({{site.url}}{{site.baseurl}}/slides/07-fastapi/fastapi.py.ipynb)
  - [Exemples](https://github.com/{{site.repository}}/tree/main/slides/07-fastapi/examples).
  - {% notebook_badges slides/07-fastapi/solutions.py.md %}
    [Solutions]({{site.url}}{{site.baseurl}}/slides/07-fastapi/solutions.py.ipynb)

### 2024-12-17 — Outils de debug et HTML

- {% notebook_badges slides/08-html/html-slides.py.md %} [Slides
  HTML]({{site.url}}{{site.baseurl}}/slides/08-html/html-slides.py.ipynb)
  - [Exemples](https://github.com/{{site.repository}}/tree/main/slides/08-html/examples)
  - {% notebook_badges slides/08-html/solutions.py.md %}
    [Solutions]({{site.url}}{{site.baseurl}}/slides/08-html/solutions.py.ipynb)
- {% notebook_badges slides/09-debug/debug-slides.py.md %} [Slides
  Debug]({{site.url}}{{site.baseurl}}/slides/09-debug/debug-slides.py.ipynb)
  - [`factorial.py`]({{site.url}}{{site.baseurl}}/slides/09-debug/factorial.py).
  - [`lintme.py`]({{site.url}}{{site.baseurl}}/slides/09-debug/lintme.py).
  - [`debugme.py`]({{site.url}}{{site.baseurl}}/slides/09-debug/debugme.py).
    - [`ancor.txt`]({{site.url}}{{site.baseurl}}/slides/09-debug/ancor.txt).

## Utilisation en local

Les supports de ce cours sont écrits en Markdown, convertis en notebooks avec
[Jupytext](https://github.com/mwouts/jupytext). C'est entre autres une façon d'avoir un historique
git propre, malheureusement ça signifie que pour les ouvrir en local, il faut installer les
extensions adéquates. Le plus simple est le suivant

1. Récupérez le dossier du cours, soit en téléchargeant et décompressant
   [l'archive](https://github.com/LoicGrobol/web-interfaces/archive/refs/heads/main.zip)
   soit en le clonant avec git : `git clone
   https://github.com/LoicGrobol/web-interfaces.git` et placez-vous dans ce dossier.
2. Créez un environnement virtuel pour le cours

   ```console
   python3 -m virtualenv .venv
   source .venv/bin/activate
   ```

3. Installez les dépendances

   ```console
   pip install -U -r requirements.txt
   ```

4. Lancez Jupyter

   ```console
   jupyter lab
   ```

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

Copyright © 2024 Loïc Grobol [\<loic.grobol@gmail.com\>](mailto:loic.grobol@gmail.com)

Sauf indication contraire, les fichiers présents dans ce dépôt sont distribués selon les termes de
la licence [Creative Commons Attribution 4.0
International](https://creativecommons.org/licenses/by/4.0/). Voir [le README](README.md#Licences)
pour plus de détails.

Un résumé simplifié de cette licence est disponible à
<https://creativecommons.org/licenses/by/4.0/>.

Le texte intégral de cette licence est disponible à
<https://creativecommons.org/licenses/by/4.0/legalcode>
