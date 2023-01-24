---
title: Interfaces web pour le TAL — M2 PluriTAL 2021
layout: default
---

[comment]: <> "LTeX: language=fr"

<!-- LTeX: language=fr -->

## News

- **2023-01-16** Les [consignes pour les projets]({{site.url}}{{site.baseurl}}/projects) sont en
  ligne.
- **2022-11-21** Premier cours du semestre le 22/11/2022.

## Infos pratiques

- **Quoi** « Interfaces web pour le TAL »
- **Où** Salle 219, bâtiment Paul Ricœur
- **Quand** 8 séances, les mardi de 13:30 à 16:30, du 22/11/22 au 24/01/23
  - Voir le planning pour les dates exactes (quand il aura été mis en ligne)
- **Contact** Loïc Grobol [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

## Liens utiles

- Lien Binder de secours :
  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/LoicGrobol/web-interfaces/main)
- [Consignes pour les projets]({{site.url}}{{site.baseurl}}/projects) sont en ligne

## Séances

Tous les supports sont sur [github](https://github.com/loicgrobol/web-interfaces), voir
[Utilisation en local](#utilisation-en-local) pour les utiliser sur votre machine comme des
notebooks. À défaut, ce sont des fichiers Markdown assez standards, qui devraient se visualiser
correctement sur la plupart des plateformes (mais ne seront pas dynamiques).

Les slides et les notebooks ci-dessous ont tous des liens Binder pour une utilisation interactive
sans rien installer. Les slides ont aussi des liens vers une version HTML statique utile si Binder
est indisponible.

### 2022-11-22 — Internet et programmation orientée objet

- {% notebook_badges slides/01-internet/internet-slides.py.md %}
  [Slides Internet](slides/01-internet/internet-slides.py.ipynb)
  - [Corrections]({{site.url}}{{site.baseurl}}/slides/01-internet/curl.sh)
- {% notebook_badges slides/02-OOP/oop-slides.py.md %}
  [Slides OOP](slides/02-OOP/oop-slides.py.ipynb)
  - [Correction CoNLL-U 1]({{site.url}}{{site.baseurl}}/slides/02-OOP/correction_conllu_v1.py)
  - [Correction CoNLL-U 2]({{site.url}}{{site.baseurl}}/slides/02-OOP/correction_conllu_v2.py)

### 2022-11-29 – Modules, requests, et HTML

- {% notebook_badges slides/03-modules/modules-slides.py.md %}
  [Slides modules](slides/03-modules/modules-slides.py.ipynb)
- {% notebook_badges slides/04-requests/requests-slides.py.md %}
  [Slides request](slides/04-requests/requests-slides.py.ipynb)
- Suivre le tutoriel [*Getting started with HTML*](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML) sur MDN

### 2022-12-06 – Parser et APIs REST

- {% notebook_badges slides/05-parsers/parsers-slides.py.md %}
  [Slides parser](slides/05-parsers/parsers-slides.py.ipynb)
  - {% notebook_badges slides/05-parsers/solutions.py.md %} [Corrections](slides/05-parsers/solutions.py.ipynb)
- {% notebook_badges slides/06-REST/rest-slides.py.md %}
  [Slides REST](slides/06-REST/rest-slides.py.ipynb)

### 2022-12-16 – Git, débuggueurs, formateurs et linters

- {% notebook_badges slides/07-git/git-slides.py.md %}
  [Slides git](slides/07-git/git-slides.py.ipynb)
- {% notebook_badges slides/08-debugger/debug-slides.py.md %}
  [Slides débuggueurs, formateurs et linters](slides/08-debugger/debug-slides.py.md)

### 2023-01-03 — Typage et FastAPI

- {% notebook_badges slides/09-fastapi/fastapi-slides.py.md %}
  [Slides FastAPI](slides/09-fastapi/fastapi-slides.py.ipynb)
  - {% notebook_badges slides/09-fastapi/solutions.py.md %}
  [Solutions](slides/09-fastapi/solutions.py.ipynb)

### 2023-01-10 — HTMl

- {% notebook_badges slides/10-html/html-slides.py.md %}
  [Slides HTML](slides/10-html/html-slides.py.ipynb)
  - {% notebook_badges slides/10-html/solutions.py.md %}
  [Solutions](slides/10-html/solutions.py.ipynb)

### 2023-01-17 — Bases de données et quelques autres choses

- {% notebook_badges slides/11-it_gen_deco/it_gen_deco-slides.py.md %}
  [Slides Itérateurs etc.](slides/11-it_gen_deco/it_gen_deco-slides.py.ipynb)
- {% notebook_badges slides/12-bdd/bdd-slides.py.md %}
  [Slides BDD](slides/12-bdd/bdd-slides.py.ipynb)

### 2023-01-24 — Quelques autres choses

- {% notebook_badges slides/12-streamlit/streamlit-slides.py.md %}
  [Slides Streamlit](slides/12-streamlit/streamlit-slides.py.ipynb)
- {% notebook_badges slides/17-js/js-slides.py.md %}
  [Slides js](slides/17-js/js-slides.py.ipynb)


## Lire les slides en local

Les supports de ce cours sont écrits en Markdown, convertis en notebooks avec
[Jupytext](https://github.com/mwouts/jupytext). C'est entre autres une façon d'avoir un historique
git propre, malheureusement ça signifie que pour les ouvrir en local, il faut installer les
extensions adéquates. Le plus simple est le suivant

1. Récupérez le dossier du cours, soit en téléchargeant et décompressant
   [l'archive](https://github.com/LoicGrobol/neural-networks/archive/refs/heads/main.zip)
   soit en le clonant avec git : `git clone
   https://github.com/LoicGrobol/neural-networks.git` et placez-vous dans ce dossier.
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
   jupyter notebook
   ```

   JupyterLab est aussi utilisable, mais la fonctionnalité slide n'y fonctionne pas pour l'instant.

## Ressources

Il y a beaucoup, beaucoup de ressources disponibles pour apprendre Python. Ce qui suit n'est qu'une sélection.

## Livres

- How to think like a computer scientist, by Jeffrey Elkner, Allen B. Downey, and Chris Meyers.
Vous pouvez l'acheter. Vous pouvez aussi le lire [ici](http://openbookproject.net/thinkcs/python/english3e/)
- Dive into Python, by Mark Pilgrim.
[Ici](http://www.diveintopython3.net/) vous pouvez le lire ou télécharger le pdf.
- Learning Python, by Mark Lutz.
- Beginning Python, by Magnus Lie Hetland.
- Python Algorithms: Mastering Basic Algorithms in the Python Language, by Magnus Lie Hetland.
Peut-être un peu costaud pour des débutants.
- Programmation Efficace. Les 128 Algorithmes Qu'Il Faut Avoir Compris et Codés en Python au Cours
  de sa Vie, by Christoph Dürr and Jill-Jênn Vie. Si le cours vous paraît trop facile. Le code
  Python est clair, les difficultés sont commentées. Les algos sont très costauds.

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

Copyright © 2021 Loïc Grobol [\<loic.grobol@gmail.com\>](mailto:loic.grobol@gmail.com)

Sauf indication contraire, les fichiers présents dans ce dépôt sont distribués selon les termes de
la licence [Creative Commons Attribution 4.0
International](https://creativecommons.org/licenses/by/4.0/). Voir [le README](README.md#Licences)
pour plus de détails.

 Un résumé simplifié de cette licence est disponible à <https://creativecommons.org/licenses/by/4.0/>.

 Le texte intégral de cette licence est disponible à <https://creativecommons.org/licenses/by/4.0/legalcode>
