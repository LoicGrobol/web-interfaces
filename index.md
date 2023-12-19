---
title: Interfaces web pour le TAL — M2 PluriTAL 2024
layout: default
---

[comment]: <> "LTeX: language=fr"

<!-- LTeX: language=fr -->

## News

- **2023-11-27** Premier cours du semestre le 28/11/2023.

## Infos pratiques

- **Quoi** « Interfaces web pour le TAL »
- **Où** Salle 410, bâtiment de la formation continue.
- **Quand** 8 séances, les mardi de 13:30 à 16:30, du 28/11/22 au 31/01/24
- **Contact** Loïc Grobol [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)
  - Demandez une invite pour le serveur Discord !

## Liens utiles

- Prendre rendez-vous pour des *office hours* en visio :
  [Calendly](https://calendly.com/lgrobol/remote-office-hour)
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

### 2023-11-28 — *Crash course* Python

- {% notebook_badges slides/01-intro_rappels/intro_rappels.py.md %} [Crash course
  python]({{site.url}}{{site.baseurl}}/slides/01-intro_rappels/intro_rappels.py.ipynb)
  - [Liste de Swadesh
    (csv)]({{site.url}}{{site.baseurl}}/slides/01-intro_rappels/data/austronesian_swadesh.csv)
  - {% notebook_badges slides/01-intro_rappels/intro_rappels-solutions.py.md %}
    [Solutions]({{site.url}}{{site.baseurl}}/slides/01-intro_rappels/intro_rappels-solutions.py.ipynb)

### 2023-12-12 — Internet et programmation orientée objet

- {% notebook_badges slides/02-internet/internet.py.md %} [Notebook
  internet]({{site.url}}{{site.baseurl}}/slides/02-internet/internet.py.ipynb)
  - [Solutions exercices cURL]({{site.url}}{{site.baseurl}}/slides/02-internet/curl.sh)
- {% notebook_badges slides/03-OOP/oop.py.md %} [Notebook
  OOP]({{site.url}}{{site.baseurl}}/slides/03-OOP/oop.py.ipynb)
  - [Treebank GSD-fr train]({{site.url}}{{site.baseurl}}/slides/03-OOP/data/fr_gsd-ud-train.conllu)
  - Solutions :
    - [Script v1]({{site.url}}{{site.baseurl}}/slides/03-OOP/correction_conllu_v1.py)
    - [Script v2]({{site.url}}{{site.baseurl}}/slides/03-OOP/correction_conllu_v2.py)

### 2023-12-19 — `requests` et APIs REST

- {% notebook_badges slides/04-requests/requests.py.md %} [Notebook
  requests]({{site.url}}{{site.baseurl}}/slides/04-requests/requests.py.ipynb)
- {% notebook_badges slides/05-REST/rest.py.md %} [Notebook
  REST]({{site.url}}{{site.baseurl}}/slides/05-REST/rest.py.ipynb)

Vos solutions pour les exercices du notebook REST sont à envoyer dans un zip à
<lgrobol@parisnanterre.fr> avant le ???. L'objet du message devra être `[Web 2024] TP Prénom Nom` et
le nom de fichier devra être de la forme `prénom_nom-établissment.zip`, `établissement` étant
`Nanterre`, `P3` ou `Inalco`.

## Utilisation en local

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
   jupyter lab
   ```

## Ressources

Il y a beaucoup, beaucoup de ressources disponibles pour apprendre Python. Ce qui suit n'est qu'une
sélection.

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

Copyright © 2023 Loïc Grobol [\<loic.grobol@gmail.com\>](mailto:loic.grobol@gmail.com)

Sauf indication contraire, les fichiers présents dans ce dépôt sont distribués selon les termes de
la licence [Creative Commons Attribution 4.0
International](https://creativecommons.org/licenses/by/4.0/). Voir [le README](README.md#Licences)
pour plus de détails.

Un résumé simplifié de cette licence est disponible à
<https://creativecommons.org/licenses/by/4.0/>.

Le texte intégral de cette licence est disponible à
<https://creativecommons.org/licenses/by/4.0/legalcode>
