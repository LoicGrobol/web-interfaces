# -*- coding: utf-8 -*-
from urllib.parse import urljoin
import sys

import httpx
from bs4 import BeautifulSoup
from bs4.element import NavigableString


def is_between_parentheses(a, p):
    n_open = 0
    for elem in p.descendants:
        if elem is a:
            break
        # On ne compte les parenthèses que dans les textes
        if isinstance(elem, NavigableString):
            n_open += elem.count("(") - elem.count(")")
    # S'il y a plus d'ouvrants que de fermants c'est pas notre problème
    return n_open > 0


def get_first_url(soup):
    """Renvoie l'addresse du premier lien du premier paragraphe dans une soupe"""
    page_contents = soup.select(".mw-parser-output")
    # On pourrait aussi faire une très grosse compréhension mais c'est déjà assez compliqué
    paragraphs = (
        p
        for content in page_contents
        for p in content.find_all("p", recursive=False)
        if p.text and not p.text.isspace()
    )
    for p in paragraphs:
        # `None` en valeur par défaut si le générateur est vide
        first_link = next(
            (
                a
                for a in p.find_all("a")
                if not a["href"].startswith("#")
                and not a.find_parents("span")
                and not a.find_parents("i")
                and not is_between_parentheses(a, p)
            ),
            None
        )
        if first_link is not None:
            return first_link["href"]
    raise ValueError("No link???")


def search_for(start_url, target_title="Philosophy"):
    next_url = start_url
    # Les initialisations bizarres c'est parce qu'on va devoir faire au moins un tour de boucle pour
    # vérifier le titre de la page de départ (utile par exemple si on est dans une redirection)
    n_hops = -1
    title = None
    # Ça devrait être marginalement plus rapide avec un set pour qui insertion et test d'inclusion
    # sont en moyenne O(1) qu'avec une liste qui est aussi en O(1) (mais plus rapide en moyenne)
    # pour l'insertion mais O(n) pour le test d'inclusion. Voir
    # <https://wiki.python.org/moin/TimeComplexity>
    visited = set()
    while title != target_title:
        n_hops += 1
        response = httpx.get(next_url, follow_redirects=True)
        soup = BeautifulSoup(response.text, "lxml")
        # Les titres sont de la forme  "{titre de page} - Wikipedia"
        title = soup.title.string.split(" - ")[0]
        # On va afficher le trajet, ça nous distraira. Pour des applications sérieuses, on utilisera
        # une bibli de log comm [loguru](https://loguru.readthedocs.io)
        print(title, file=sys.stderr)
        # On a trouvé un cycle
        if title in visited:
            # On sait que c'est pas `target_title` sinon on serait sorti de la boucle avant,
            # puisqu'on l'a déjà visité. On peut donc être certain⋅e⋅s qu'on atteindra jamais la
            # cible. Plutôt que de faire des fantaisies à renvoyer `math.inf` ou je ne sais quoi, on
            # va sobrement renvoyer `-1`. On pourrait aussi lever une exception.
            return -1
        visited.add(title)
        next_url = urljoin(next_url, get_first_url(soup))
    return n_hops


if __name__ == "__main__":
    target = "Philosophy" if len(sys.argv) == 2 else sys.argv[2]
    n_hops = search_for(sys.argv[1], target)
    if n_hops < 0:
        print(f"Couldn't get to {target}")
    else:
        print(n_hops)
