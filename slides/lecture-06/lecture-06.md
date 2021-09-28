---
jupyter:
  jupytext:
    formats: ipynb,md
    split_at_heading: true
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.0
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

[comment]: <> "LTeX: language=fr"

<!-- #region slideshow={"slide_type": "slide"} -->
Cours 6 : Internet, Web et HTTP
===============================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)

2021-09-29
<!-- #endregion -->

```python
%matplotlib widget

import matplotlib.pyplot as plt
import numpy as np
import scipy.special
import codecs

from IPython.display import display, Markdown
```

Dans ce cours, on va faire une très, très rapide introduction aux concepts réseaux et web qui
sous-tendent le reste de ce qu'on va faire dans ce cours. Par nécessité on ne fera que gratter la
surface de la partie émergée de l'iceberg et il vous restera après beaucoup de choses à apprendre ou
à préciser sur le fonctionnement d'Internet et du Web. N'hésitez surtout pas à vous documenter de
votre côté.

Les ressources de la [MDN web doc](https://developer.mozilla.org), communautaires et de très grande
qualité sont un bon point de départ.

## Une vidéo pour se réveiller

[![L'hémisphère nord de la terre vu de l'espace, parcouru par des câbles reliant différent types de
serveurs et sur lesquels transitent des blocs de 0 et de 1. Une antenne relais transmet un signal au
smartphone d'une personne qui porte une robe rouge et on voit une image corrompue de la page
d'accueil de Google et une représentation d'un de leurs
datacenters.](https://img.youtube.com/vi/x3c1ih2NJEg/hqdefault.jpg)](https://youtu.be/x3c1ih2NJEg)

Clique sur l'image, c'est un lien.

## Internet, c'est quoi ?

Adapté de [la documentation web du
MDN](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/How_does_the_Internet_work).

### Historique très rapide d'Internet

- Années 1940 — 1950 : les ordinateurs sont **massifs** et peu nombreux. Pour des raisons de
  facilités on y accède donc depuis des terminaux distants
  - De plus en plus distants
  - On développe petit à petit des technologies pour augmenter la vitesse et la fiabilité des
    communications numériques à longue distance
- Années 1960 : l'idée d'interconnecter des ordinateurs entre eux pour le partage d'informations
  apparait graduellement
- 1969 : premier réseau effectif entre machines, ARPANET, financé par l'Agence pour les projets de
  recherche avancée de défense (DARPA) du département de la Défense des États-Unis
  - Rapidement suivi par d'autres initiatives ailleurs dans le monde
- 1970 – 2000 : émergence de nouveaux réseaux locaux et régionaux, progressivement fusionnés pour
  donner un réseau global, Internet.

Pour plus de détails, la source la plus riche que j'ai trouvée est [l'article *History of Internet*
de Wikipédia en anglais](https://en.wikipedia.org/wiki/History_of_the_Internet).

### Réseaux de machines

Mettre deux machines en réseau, c'est (conceptuellement) simple, on appelle ça une connexion
point-à-point.

![Deux ordinateurs, nommés A et B reliés par un câble](pics/internet-schema-1.png)

Et théoriquement, c'est possible de le faire pour autant de machines qu'on veut

![Dix ordinateurs, nommés A, …, J, disposés en cercle et reliés chacun à tous les autres par un réseau de câbles](pics/internet-schema-2.png)

Mais ça fait beaucoup de câbles et de prises. Combien d'ailleurs ?

```python
fig = plt.figure()
plt.plot(scipy.special.binom(np.arange(2, 64, 1), 2), "o");
plt.xlabel("Nombre de machines dans le réseau")
plt.ylabel("Nombre de câbles nécessaires")
```

Pour éviter ça, on peut plutôt avoir une machine qui sert de centre (ou *hub*). Le plus souvent ce
sera une machine spécialisée, qu'on appelle *routeur*. Chaque machine du réseau est alors reliée
seulement au hub.

![Dix ordinateurs, nommés A, …, J, disposés en cercle et tous reliés à une machine centrale](pics/internet-schema-3.png)

On parle alors de réseau *en étoile*. Ça permet de simplifier considérablement le réseau. Dans ce
cas, quand A passe un message à B, il le passe d'abord au hub (en lui disant que le destinataire est
B) et le routeur le passe à B.

Il existe d'autres types de réseaux (on parle de *topologie*), le plus important étant les réseaux
en anneau, qui ne nécessitent pas de centre mais sont moins efficaces.

On peut aussi connecter entre eux des réseaux de ce type, en formant des arbres

![Dix ordinateurs, nommés A, …, O, disposés en arbres avec A, …, E connectés à un routeur, F, …, J à
un autre et K, …, O à un troisième et ces routeurs connectés à un routeur
central](pics/internet-schema-5.png)

Cette idée de réseaux locaux interconnectés en arborescence pour former un réseau global est le
principe de base d'internet, qui en pratique est plus complexe que ça, avec notamment des liens
redondants qui le rendent plus modulable en fonction du trafic et plus robuste en cas
d'interruption.

## Protocoles de communication

La topologie d'un réseau nous donne la façon dont les machines sont connectées entre elles, mais pas
comment elles communiquent.

Dans une optique de *séparation des préoccupations*, la façon dont ces communications opèrent est
divisée en une pile de protocole, du plus près du matériel au plus près des utilisateurices. Chaque
couche de protocole traite d'un aspect bien déterminé, sans se préoccuper du fonctionnement interne
des couches inférieures et supérieures.

Dans le modèle TCP/IP, on distingue en général quatre couches

- La couche *applicative* concerne la façon dont une application sur une machine A communique avec
  une application sur une machine B. On y suppose que chacune des deux applications a accès à une
  interface sur laquelle elle peut envoyer et recevoir des données en sachant qu'elles seront
  correctement transmises à l'autre application. C'est surtout ce niveau qui va nous intéresser.
- La couche *de transport* définie la façon dont deux machines sur un réseau communiquent. On y
  suppose que chaque machine a accès à une interface permettant de passer des message à l'autre
  machine.
- La couche *internet* concerne la façon dont des réseaux déjà existants peuvent établir des
  communications entre eux et les utiliser pour se passer des messages via leurs routeurs.
- La couche *de lien* concerne la façon dont les données transitent sur un réseau entre les machines
  de ce réseau et leur routeur ou entre deux routeurs.

Imaginons (en simplifiant) qu'une application a sur une machine A veuillent passer un message à une
application b sur une machine B. Elle place ce message dans un paquet HTTP (applicatif), et le
confie à l'interface réseau de A, qui va le placer dans un paquet TCP (transport) et la transmettre
à son routeur (avec lequel elle communique sur la couche de lien). Le routeur va alors déterminer le
trajet que doit effectuer le paquet pour aller jusqu'à B et le transmettre (couche internet). Le
paquet arrive au routeur de B qui le transmet à b en suivant les étapes en sens inverse.

D'autres couches peuvent venir s'y intercaler. Par exemple pour des communications sécurisées, le
protocole TLS vient s'intercaler entre la couche transport (TCP) et la couche applicative (HTTP).

![](pics/http-layers.png)

### Adresse IP et noms de domaine

Chaque machine est identifiée sur le réseau Internet de manière unique par son IP. Vous pouvez
trouver la vôtre avec la commande `ip`

```python
! ip addr
```

Votre adresse IP (v4) se lit dans `inet` et votre adresse IP (v6) dans `inet6`. Comparez vos
adresses entre vous et avec l'adresse que vous donne par exemple <https://whatismyipaddress.com/>,
que constatez-vous ?

Quel site se trouve à l'adresse suivante :

```python
mysterious_ip, *_ = !dig +short {codecs.decode("jjj.gny.havi-cnevf3.se", "rot13")} | tail -n 1
Markdown(f"<http://{mysterious_ip}>")
```

Il n'est évidemment pas pratique de travailler directement avec les adresses IP pour accéder à des
machines publiques.

- Compliquées à retenir
- Ne permet pas d'héberger plusieurs services sur une même machine ou un même service sur plusieurs
  machines.

On fonctionne donc avec un système de *noms de domaines* qui ajoute une couche d'indirection : pour
accéder à une machine on demande à un serveur de noms de domaines (DNS) l'adresse qui correspond à
une chaîne de caractères : son nom de domaine. Comme :

- <http://python.net>
- <http://plurital.org>
- <http://w3c.org>

Voir par exemple [la doc du MDN](pour plus d'infos sur les noms de domaine).

### Routage

On ne va pas rentrer dans les détails de fonctionnement du routage, mais on peut se faire une idée
du trajet que suivent les données pour aller de votre machine à une autre avec la commande
`traceroute` (il vous faudra peut-être l'installer)

```python
!traceroute python.net
```

### Paquets

La sortie de `traceroute` parlait de « *packets* », de quoi s'agit-il ?

Une des idées qui a permis l'établissement d'Internet est celle de découper les données à passer
d'une machine à une autre en séries de paquets au niveau de la couche de transport (typiquement dans
les protocoles TCP et UDP). Ça rend les communications plus robustes :

- Tous les paquets n'ont pas besoin de passer par le même chemin.
- Si un paquet est perdu ou corrompu, il suffit de renvoyer **ce** paquet.

Un paquet est composé de :

- Un *header* qui contient une série de métadonnées qui dépende du protocole mais indique au moins
  la destination et un identifiant du paquet.
- Un *payload* qui contient les données ou le fragment de données à transmettre.

Cette division va se retrouver dans d'autres couches, par exemples elle concerne également les
requêtes et réponses en HTTP.

## Le Web

Le World Wide Web, ou web, est un système d'information reposant sur Internet, constitué de
documents et de ressources, possédant des *Universal Resource Locators* (URL), des chaînes de
caractères qui permettent d'y accéder de façon stable depuis n'importe quel point d'accès.

Une URL est habituellement de la forme `http://www.example.com/path/page.html`, où `http` désigne le
protocole applicatif suivant lequel la ressource est mise à disposition, `www.example.com` est le
nom de domaine associé à une machine qui met la ressource à disposition et `path/page.html` est un
chemin interne à cette machine, qui peut correspondre ou non à un chemin dans son système de
fichiers.

→ Voir aussi le concept d'[URI](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier).

Une des particularités du Web est sa construction sur le concept d'hypertextualité : les documents
auquel il permet d'accéder sont prévus pour être des documents textuels — habituellement structurés
et décrits en langage HTML — mais surtout liés par des *liens hypertexte* : des URL de documents ou
de ressources liées. Ainsi, ce qu'on appelle un *site web* ou *site Internet* est conceptuellement
simplement un ensemble cohérent de documents textuels (ou *pages web*) liées par des liens
hypertextes

## HTTP

Le *HyperText Transfer Protocol* est un protocole de la couche applicatif qui a été créé pour le
Web. Comme la plupart des autres protocoles, il a connu plusieurs versions, la plus récente étant
HTTP/3.

Ses caractéristiques principales, liées à son objectif initial de relier des pages d'hypertextes
sont d'être :

- Textuel : les données et métadonnées sont transmises sous forme de données en texte, donc en
  chaînes de caractères.
- Simple : les messages passés via HTTP sont censés pouvoir être lu et facilement compris par des
  humain⋅e⋅s
- Sans mémoire (stateless) : chaque message est indépendant des précédents, ce qui signifie que deux
  messages identiques devraient avoir des effets identiques.

Ces principes sont en pratique plus souple : il n'est pas inhabituel de transmettre des données
non-textuelles en les représentant sous forme de chaîne de caractères et en pratique, il est très
courant d'implémenter des protocoles à mémoire (*stateful*) en surcouche d'HTTP (par exemple au
moyen de [jetons](https://fr.wikipedia.org/wiki/Identificateur_de_session) et de
[cookies](https://fr.wikipedia.org/wiki/Cookie_\(informatique\)).

### Un exemple

Un exemple avec la commande cURL (qu'il vous faudra peut-être installer)

```python
!curl -v https://kde.org
```

On peut y voir

- Une résolution de nom de domaine
- Une négociation de protocole de communication
- Une négociation de protocole de sécurité
  - Vérification de l'identité du site
  - Échange de clés pour une communication chiffrée
- L'envoi d'une requête `GET` : demande de page
- La réponse du serveur, contenant des *headers* et un *payload* : une page en HTML, qui contient
  elle-même des métadonnées, du contenu, des informations de style et du code JavaSCript qui permet
  de la rendre interactive en local (le code étant prévu pour être exécuté sur les machines des
  destinataires de la page).

Si on accède habituellement à des pages web à partir d'un navigateur qui propose une interface
graphique, ce n'est pas en soi une obligation (puisque tout ce qui compte ce sont les message
passés), et des outils comme cURL ou les scripts que nous allons écrire peuvent très bien
fonctionner sans.

→ Voir [le tutoriel de cURL](https://curl.se/docs/httpscripting.html). Voir aussi
[wget](https://www.gnu.org/software/wget/), un autre outil qui permet de formuler des requêtes HTTP.

### Requêtes et réponses

Le protocole HTTP est construit sur la notion qu'il existe deux rôles pour les machines connectées :

- Les serveurs sont les machines où les documents et les ressources sont mises à disposition
- Les clients sont les machines des utilisateurices qui désirent accéder à ces documents et
  ressources

Le rôle d'une machine donnée n'est pas constant (même si certaines machines sont plus adaptées pour
un rôle que pour l'autre), mais est pris de façon *ad-hoc* pour chaque connexion.

De ce fait, dans une communication HTTP, les messages passés entre les machines sont asymétriques

- Le client envoie des *requêtes* au serveur
- Le serveur envoie des *réponses* au client

![Un schéma de la relation client-serveur : un cercle représente le client, un autre le serveur. Une
flèche étiquetée « requests » va du client vers le serveur et une flèche étiquetée « responses » va
du serveur vers le client.](pics/simple-client-server.png)

### Types de requêtes

Les requêtes HTTP sont regroupées par type, en fonction du type d'action qu'elles demandent au
serveur. Les plus importantes pour nous sont :

- `GET` demande une ressource au serveur, c'est la requête utilisée pour récupérer une page web par
  exemple.
- `POST` envoie des données au serveur sous forme d'une modification cumulative. C'est la requête
  utilisée par exemple pour envoyer des formulaires. Si on envoie plusieurs fois la même requête
  `POST` au serveur, il est censé exécuter autant de fois la même action.
- `PUT` envoie des données au serveur sous forme d'un état. C'est la requête habituellement utilisée
  pour envoyer des ressources. Si on envoie plusieurs fois la même requête `PUT` au serveur, le
  résultat est censé être le même que si on ne l'avait envoyée qu'une seule fois.

→ Voir [la liste complète sur MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods).

La différence entre `POST` et `PUT` est un peu ésotérique et en pratique elles sont souvent
utilisées l'une pour l'autre.