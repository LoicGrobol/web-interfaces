---
jupyter:
  jupytext:
    cell_metadata_filter: slideshow,-all
    formats: ipynb,md
    split_at_heading: true
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.0
  kernelspec:
    display_name: cours-web (3.14.0)
    language: python
    name: python3
---


<!-- LTeX: language=fr -->

<!-- #region slideshow={"slide_type": "slide"} -->
Cours N : NodeJS
================

**L. Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)
<!-- #endregion -->


## NodeJS

[NodeJS](https://nodejs.org) a été la première plateforme permettant d'utiliser JavaScript non
seulement comme langage web interprété dans un navigateur (*frontend*), mais aussi comme langage de
script système, avec le but principal de l'utiliser pour construire des serveurs (*backend*).

Depuis des alternatives sont apparues, comme [Deno](https://deno.com) (porté par le créateur de
NodeJS) ou [Bun](https://bun.com) (développé par Anthropic). À titre personnel, j'ai tendance à
préférer Deno, **mais** comme d'habitude les écosystèmes ont beaucoup d'inertie, et pour l'instant,
si vous avez à utiliser du JavaScript côté serveur, c'est probable que ce soit en Node. Dans tous
les cas, ces alternatives se sont principalement construites en *réaction* à Node et lui restent
largement similaires — donc rien à perdre à commencer par apprendre Node.

Note : Contrairement à Python, NodeJS n'a *ostensiblement* pas été pensé pour l'enseignement ou pour
débuter en programmation. La documentation est assez peu ergonomique et les interface sont
optimisées pour les performances plus que pour la lisibilité. Attendez-vous donc à trouver plus
confus et désagréable que l'écosystème Python.

### Structure

On travaille comme souvent avec un mille-feuille, en résumé :

- Vous écrivez un fichier `.js`, qui contient du code en JavaScript.
  
  ```js
  console.log("Hello, world!")
  ```

- Vous l'interprétez avec Node
  
  ```bash
  node examples/hello.hello.js
  ```

Comme en Python, facile !

En arrière-plan, Node va :

- Lire et compiler votre fichier via [V8](https://v8.dev/), le moteur JavaScript qui est aussi
  utilisé entre autres par Chrome et Edge
- Traduire les fonctions comme `readFile` en appels systèmes
- Exécuter votre code


### Installer Node

Plusieurs options :

- Installer `nodejs` directement via votre gestionnaire de paquets systèmes (`apt`, `pacman`,
  `brew`…)
  - Facile et simple
  - Les mises à jour peuvent être décalés et la sélection d'une version précise compliquée.
  - L'équivalent d'un `apt install python3`
- Installer `pnpm`, qui est un gestionnaire d'environmment pour Node (l'équivalent de `uv`) et
  invoquer Node avec `pnpx node`
  - Permet de choisir la version de Node avec laquelle on travaille
  - Il vous faudra de toute façon un gestionnaire d'environnement et celui-ci est le meilleur.
