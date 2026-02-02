---
title: Projets Interfaces web pour le TAL 2026
layout: default
permalink: /projects/
---

[comment]: <> "LTeX: language=fr"

Projets
========

Votre travail sera de réaliser une interface web en Python pour un système de TAL, de traitement ou
d'accès à des données. Elle devra au moins comprendre une interface programmatique sous la forme
d'une API REST utilisable par un serveur ASGI (c'est par exemple le cas de celles réalisée en
FastAPI que vous avez vues en cours) et une interface utilisateur qui pourra prendre la forme d'un
script ou très, très préférablement d'une interface web HTML + CSS [+ js]

Ce projet peut évidemment être en lien avec d'autres cours, d'autres projets ou votre travail en
entreprise (mais assurez-vous avant que ce soit OK de partager votre code avec moi dans ce cas).

On peut éventuellement relaxer ces exigences si vous avez une idée spécifique, mais commencez par
m'en parler avant.

Contrainte spécifique pour 2026 : pas de chatbot ou d'interface pour LLM. Vous en voyez déjà bien
assez par ailleurs, ça vous changera les idées.

## Consignes

- Composition des groupes et sujets des projets à envoyer avant le 07 février 2026 (envoyer un mail
  par groupe avec vos noms, prénoms et établissements et une description concise, mais précise du
  projet). Si vous avez un doute sur la pertinence ou la faisabilité du projet, venez m'en parler
  avant.
- Projet à rendre le 15 mars 2026 *au plus tard*
- Projet de préférence collectif, par groupe de 2 ou 3
  - Si c'est un problème pour vous, venez me voir, tout est négociable
  - S'il y a un problème — quel qu'il soit — dans votre groupe, n'hésitez pas à m'en parler
- Rendus par mail à `lgrobol@parisnanterre.fr` avec en objet `[web2026] Projet final` et les noms,
  prénoms et établissements de tous les membres du groupe dans le corps du mail.
  - **Si l'objet est différent, je ne verrai pas votre rendu**. Et si un nom manque, vous risquez de
    ne pas avoir de note.
  - **Les noms de tous les membres du projet doivent apparaître dans la documentation.**
  - J'accuserai réception sous trois jours ouvrés dans la mesure du possible, relancez-moi si ce
    n'est pas le cas.


Le rendu devra comporter :

1. Une documentation du projet traitant les points suivants :

   - Les objectifs du projet
   - Une description du système ou des données auxquelles l'interface permet d'accéder
   - La méthodologie (comment vous vous êtes répartis le travail, comment vous avez identifié les
     problèmes et les avez résolus, différentes étapes du projet…)
   - L'implémentation ou les implémentations (modélisation le cas échéant, modules et/ou API
     utilisés, différents langages le cas échéant)
   - Les résultats (fichiers output, visualisations…) et une discussion sur ces résultats (ce que
     vous auriez aimé faire et ce que vous avez pu faire par exemple)

   On attend de la documentation technique, pas une dissertation. Elle pourra prendre le format d'un
   ou plusieurs fichiers, d'un site web, d'un notebook de démonstration, à votre convenance

   **La documentation ne doit pas, jamais, sous aucun prétexte, comporter de capture d'écran de
   code.**

2. Le code Python et les codes annexes (JS par ex.) que vous avez produit. Le code *doit* être
   commenté. **Évitez les notebooks** (de toute façon ce n'est pas idéal pour des interfaces web).

3. Les éventuelles données en input et en output (ou un échantillon si le volume est important)

N'hésitez pas à vous servir de git pour versionner vos projets !

## Conseils

Écrivez ! Tenez un carnet : vos questions, un compte-rendu de vos discussions,
les problèmes rencontrés, tout est bon à prendre et cela vous aidera à rédiger
la documentation finale.

## Ressources

### Hébergement

- [Python Anywhere](https://help.pythonanywhere.com/pages/Education)

### Données géo-localisées

Il existe beaucoup de choses pour travailler avec des données géo-localisées. Allez voir en vrac :
[Geo-JSON](http://geojson.org/), [uMap](http://umap.openstreetmap.fr/fr/) pour créer facilement des
cartes en utilisant les fonds de carte d'OpenStreetMap, [leaflet](http://leafletjs.com/) une lib JS
pour les cartes interactives, [overpass turbo](http://overpass-turbo.eu/) pour interroger facilement
les données d'OpenStreetMap (il y a une [api !](http://www.overpass-api.de/)).

### Ressources linguistiques

N'hésitez pas à aller fouiller dans [Ortolang](https://www.ortolang.fr/) ou
[Clarin](https://lindat.mff.cuni.cz/repository/xmlui/) des ressources linguistiques exploitables
librement et facilement. Vous pouvez aussi aller voir du côté de l'API twitter pour récupérer des
données (qui ne sont pas nécessairement uniquement linguistiques)

### Open Data

Quelques sources : [Paris Open Data](https://opendata.paris.fr),
[data.gouv.fr](https://data.gouv.fr), [Google dataset
search](https://toolbox.google.com/datasetsearch)

## Idées

### Accès aux données

Réaliser une interface pour exploiter une ressource (linguistique ou autre).

- Soit en rendant lisible des données massives en faisant des stats
- Soit en faisant apparaître des représentations pertinentes de données
  individuelles complexes (syntaxe, entités nommées, sentiment…)

### Interfaces systèmes

Réaliser une interface permettant d'accéder facilement à un système de TAL, dans l'esprit de
[UDPipe](https://lindat.mff.cuni.cz/services/udpipe/) par exemple.
