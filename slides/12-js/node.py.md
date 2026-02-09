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
      jupytext_version: 1.19.1
  kernelspec:
    display_name: cours-web
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
optimisées pour les performances plus que pour la lisibilité. Attendez-vous donc à trouver ça plus
confus et désagréable que l'écosystème Python.

### Structure

On travaille comme souvent avec un mille-feuille, en résumé :

- Vous écrivez un fichier `.js`, qui contient du code en JavaScript.
  
  ```js
  console.log("Hello, world!")
  ```

- Vous l'interprétez avec Node
  
  ```bash
  node examples/hello.js
  ```

Comme en Python, facile !

En arrière-plan, Node va :

- Lire et compiler votre fichier via [V8](https://v8.dev/), le moteur JavaScript qui est aussi
  utilisé entre autres par Chrome et Edge
- Traduire les fonctions comme `readFile` en appels systèmes
- Exécuter votre code


<!-- #region -->
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

### Ressources

- [Le tutoriel de Node](https://nodejs.org/en/learn/getting-started)
- [L'« API » de Node](https://nodejs.org/api/) (en Python on dirait « bibliothèque standard »)
<!-- #endregion -->

<!-- #region -->
### ☕ Entraînement ☕

#### Bonjour tout le monde

Créez un `hello.js` qui afficher `Hello, world!` dans la console et exécutez le avec Node.
<!-- #endregion -->

<!-- #region -->
#### Un serveur

1\. Créez un `server.js` avec le contenu suivant, et exécutez-le

```js
import { createServer } from "node:http"

const hostname = "localhost"
const port = 3000

const server = createServer((req, res) => {
    res.statusCode = 200
    res.setHeader("Content-Type", "text/plain")
    res.end("Hello World")
})

server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`)
})
```

2\. Testez si le serveur est accessible (par exemple avec cURL), puis modifiez le code pour lui
faire plutôt renvoyer le JSON suivant :

```json
{"message": "Bonjour tout le monde !"}
```

3\. Modifiez le code pour afficher à chaque requête un message dans la console (pour l'instant juste
une chaîne de carctères constante)

4\. Le paramètre `req` du callback de `createServer` est de type
[`http.IncomingMessage`](https://nodejs.org/api/http.html#class-httpincomingmessage). À l'aide de la
documentation, ajoutez au message que vous loggez dans la console la méthode de la requête reçue
(`GET`, `POST`…).
<!-- #endregion -->

<!-- #region -->
### Modules

Comme tout en JavaScript, l'histoire des modules et des imports est un peu compliquée. De nos jours,
cependant, il existe une solution *standard*, qui marche dans Node et dans les navigateurs [les modules dits « ESM »](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules). Allez voir le lien précédent pour les détails du fonctionnement. L'essentiel est dans la ligne d'import de l'exercice précédent :

```javascript
import { createServer } from "node:http"
```

Qui comme en Python signifie « importe l'objet nommé `createServer` dont la définition est dans le
module `node:http`.

(Le prefixe `node:` est un marqueur de protocole. Vous pouvez aller voir [la
doc](https://nodejs.org/api/esm.html#node-imports) pour les détails mais ça ne devrait pas être
immédiatement crucial pour nous).
<!-- #endregion -->

<!-- #region -->
## Environnements et paquets

Comme pour Python, même si la bibliothèque standard de Node est bien fournie, il vous faudra tôt ou
tard dépendre du code d'autres gens. Par exemple pour *padder* une chaîne de caractères, on peut utiliser le modulde [`pad-left`](https://www.npmjs.com/package/pad-left) dont voici un exemple :

```javascript
import pad  from "pad"

console.log(pad("2713", 8, "0"))
```

Si vous l'exécutez comme ça, Node va vous renvoyer une erreur `ERR_MODULE_NOT_FOUND`, car `pad` n'est pas installé.

(Pourquoi `import pad` et pas `import { pad }` ? Parce que c'est un export par défault et pas un
export nommé. Allez voir
[MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules#default_exports_versus_named_exports).
Oui c'est pénible.)
<!-- #endregion -->

<!-- #region -->
Pour installer un module avec PNPM, faites tout simplement :

```bash
pnpm install "pad"
```

Ceci va créer des nouveaux fichiers dans le dossier courant (où `padd.js` est mon script):

```text
.
├── node_modules/
├── package.json
├── padd.js
└── pnpm-lock.yaml
```
<!-- #endregion -->

 Dans `node_modules`, il ya ce qui ressemble à un environnement virtuel de Python : le contenu du package `pad` (allez voir son `index.js`) ainsi que des métadonnées.


Voici le contenu de `package.json`

```json
{"dependencies":{"pad":"^3.3.0"}}
```


Enfin `pnpm-lock.yaml`, qui n'est vraiment pas fait pour être écrit (et même pas vraiment lu) par des humain⋅es est un *lockfile* : il enregistre les version exactes de tous les paquets installés dans l'environnement avec des hash qui permettent de vérifier leur intégrité.


`node_modules` fonctionne comme un environnement virtuel implicite : quand vous exécutez un script
avec Node, celui-ci va chercher dans les dossiers adjacents et parents les dossiers `node_modules`
et aller y chercher les paquets que vous importez.


`package.json` fonctionne comme un `pyproject.toml`, en un peu plus flexible. A minima il permet de lister vos dépendances (comme dans la version ici générée par `pnpm`), mais il permet aussi de saisir les métadonnées d'un package à publier sur [npmjs.com](https://npmjs.com) ou un index similaire (les équivalents de PyPI). On peut aussi l'utiliser pour configurer des outils de développement, définir des commandes… Voyez par exemple le `package.json` de `pad` :

```json
{
  "name": "pad",
  "description": "Left and right string padding",
  "version": "3.3.0",
  "author": "David Worms <david@adaltas.com> (https://www.adaltas.com)",
  "contributors": [],
  "devDependencies": {
    "@commitlint/cli": "^19.5.0",
    "@commitlint/config-conventional": "^19.5.0",
    "@eslint/core": "^0.6.0",
    "@eslint/js": "^9.11.1",
    "@rollup/plugin-commonjs": "^28.0.0",
    "@rollup/plugin-node-resolve": "^15.3.0",
    "@rollup/plugin-terser": "^0.4.4",
    "@types/eslint__js": "^8.42.3",
    "@types/mocha": "^10.0.8",
    "@types/node": "^22.7.4",
    "@types/should": "^13.0.0",
    "coffeescript": "^2.7.0",
    "eslint": "^9.11.1",
    "eslint-config-prettier": "^9.1.0",
    "eslint-plugin-mocha": "^10.5.0",
    "eslint-plugin-prettier": "^5.2.1",
    "husky": "^9.1.6",
    "lint-staged": "^15.2.10",
    "mocha": "^10.7.3",
    "prettier": "^3.3.3",
    "rollup": "^4.22.5",
    "rollup-plugin-commonjs": "^10.0.0",
    "rollup-plugin-delete": "^2.1.0",
    "rollup-plugin-dts": "^6.1.1",
    "rollup-plugin-node-resolve": "^5.0.0",
    "rollup-plugin-typescript2": "^0.36.0",
    "should": "^13.2.3",
    "standard-version": "^9.5.0",
    "ts-node": "^10.9.2",
    "typescript": "^5.6.2",
    "typescript-eslint": "^8.7.0"
  },
  "dependencies": {
    "wcwidth": "^1.0.1"
  },
  "optionalDependencies": {
    "@rollup/rollup-linux-x64-gnu": "4.9.5"
  },
  "engines": {
    "node": ">= 4.0.0"
  },
  "exports": {
    ".": {
      "import": "./dist/esm/index.js",
      "types": "./dist/types/index.d.ts",
      "require": "./dist/cjs/index.cjs"
    }
  },
  "homepage": "https://github.com/adaltas/node-pad",
  "keywords": [
    "pad",
    "string"
  ],
  "files": [
    "/dist"
  ],
  "license": "BSD-3-Clause",
  "lint-staged": {
    "*.js": "npm run lint:fix",
    "*.md": "prettier -w"
  },
  "mocha": {
    "inline-diffs": true,
    "loader": "ts-node/esm",
    "recursive": true,
    "reporter": "spec",
    "require": [
      "should"
    ],
    "throw-deprecation": false,
    "timeout": 40000
  },
  "module": "dist/pad.esm.js",
  "repository": {
    "type": "git",
    "url": "https://github.com/adaltas/node-pad.git"
  },
  "scripts": {
    "build": "rollup -c",
    "lint:check": "eslint",
    "lint:fix": "eslint --fix",
    "lint:staged": "npx lint-staged",
    "release": "standard-version",
    "release:minor": "standard-version --release-as minor",
    "release:patch": "standard-version --release-as patch",
    "release:major": "standard-version --release-as major",
    "postrelease": "git push --follow-tags origin master",
    "test": "mocha test/*.{js,ts}",
    "prepare": "husky install"
  },
  "type": "module"
}
```


Dans l'immédiat ce n'est pas forcément crucial pour vous : vous pouvez juste vous servir de `pnpm`
pour ajouter, retirer ou mettre à jour des dépendances. Par ailleurs si vous êtes dans un dossier
avec un `package.json`, `pnpm install` installera directement toutes les dépendances que vous y
déclarez.


Comme avec `pip`, il est possible d'installer des packages *globalement* avec PNPM. Comme avec pip, ce n'est pas forcément une bonne idée. Si vous en sentez le besoin, je vous recommande plutôt d'utiliser `pnpx`.

### 🎨 Entraînement 🎨

En utilisant [yoctocolors](https://www.npmjs.com/package/yoctocolors) ajoutez de la couleur à votre serveur.

## npm sur le front

De nos jours c'est aussi assez courant d'utiliser (p)npm comme gestionnaire de paquets pour du frontend. Vous pouvez par exemple aller voir [Vite](https://vite.dev/guide/) ou [Rollup](https://rollupjs.org/introduction/) pour un exemple d'outillage pour ça.
