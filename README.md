[comment]: <> "LTeX: language=fr"
<!-- markdownlint-disable MD003 MD025 MD033 -->

Interfaces web pour le TAL
==========================

[![Licence : CC BY 4.0](https://licensebuttons.net/l/by/4.0/80x15.png)](https://creativecommons.org/licenses/by/4.0/)

Contenus pour le cours « Bases de données et web dynamique » du master [Plurital](http://plurital.org).


- [Site du cours](https://loicgrobol.github.io/web-interfaces/)
- [Dépôt GitHub](https://github.com/LoicGrobol/web-interfaces)

Contact : [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

## Générer le site en local

Dependencies:

- Ruby
  - Bundle

Setup:

```console
gem install jekyll bundler
bundle config set --local path 'vendor/bundle'
bundle install
```

Regenerate:

```bash
bundle exec jekyll build
bundle exec jekyll serve
```

Astuce pour les pages : Jekyll n'est pas très bon pour les pages qui ne sont pas des postes de blog,
les ajouter dans `_pages` (ce qui fonctionne parce qu'on l'a mis dans `_config.yml`) et leur donner
un `permalink` dans le header.

## Licences

[![CC BY Licence badge](https://i.creativecommons.org/l/by/4.0/88x31.png)](http://creativecommons.org/licenses/by/4.0/)


Copyright © 2025 Loïc Grobol [\<lgrobol@parisnanterre.fr\>](mailto:lgrobol@parisnanterre.fr)

Sauf indication contraire, les fichiers présents dans ce dépôt sont distribués selon les termes de
la licence [Creative Commons Attribution 4.0
International](https://creativecommons.org/licenses/by/4.0/).

Un résumé simplifié de cette licence est disponible à <https://creativecommons.org/licenses/by/4.0/>.

Le texte intégral de cette licence est disponible à
<https://creativecommons.org/licenses/by/4.0/legalcode>

## Exceptions à la licence

Les fichiers suivants ne sont pas distribués selon les termes de la licence Creative Commons
Attribution 4.0 International

### CC-BY-SA

[![CC-BY-SA Licence
badge](https://i.creativecommons.org/l/by-sa/2.5/88x31.png)](http://creativecommons.org/licenses/by-nc-nd/4.0/)

- Les images `internet-schema-*.png` et `simple-client-server.png` du dossier
  [`slides/lecture-06/pics`](slides/lecture-06/pics) sont issues [de la documentation web du
  MDN](https://github.com/mdn/content) sont soumises à la licence [CC-BY-SA
  2.5](https://creativecommons.org/licenses/by-sa/2.5/).