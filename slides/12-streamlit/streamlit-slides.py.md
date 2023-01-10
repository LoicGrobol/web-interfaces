---
jupyter:
  jupytext:
    formats: ipynb,md
    split_at_heading: true
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.1
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- LTeX: language=fr -->

<!-- #region slideshow={"slide_type": "slide"} -->
Cours 12 : Interfaces magiques avec Streamlit
=============================================

**Loïc Grobol** [<lgrobol@parisnanterre.fr>](mailto:lgrobol@parisnanterre.fr)
<!-- #endregion -->

Ce document est très fortement inspiré du tutoriel [*Streamlit 101: An in-depth introduction*](https://towardsdatascience.com/streamlit-101-an-in-depth-introduction) et du [tutoriel de Streamlit](https://docs.streamlit.io/library/get-started).

```python
from IPython.display import display
```

On a vu jusqu'ici comment faire des interfaces **programmatiques** et des interfaces **graphiques
web** directement en HTML.


C'est très bien et on peut tout faire avec ça — avec assez de patience et d'étude des technos web.


Cependant, il existe des alternatives, qui permettent pour des cas d'usages restreints d'obtenir
directement des interfaces sophistiquées avec très peu d'efforts.


On va parler ici de celle qui a le plus de succès récement et la plus intéressante pour nous : Streamlit.


## Streamlit ?

[Streamlit](https://streamlit.io).


```python
%pip install -U streamlit
```


Streamlit est une bibliothèque de développement d'interfaces web spécialisée dans les interfaces
d'accès aux données. Elle permet d'écrire très rapidement des interfaces sans écrire de code web, en
traduisant directement du code en Python, avec beaucoup de magie pour que ce soit fluide.

Comment ça marche concrètement ? Et bien voici une application Streamlit

```python
# %load apps/slider.py
import streamlit as st
x = st.slider("x")
st.write(x, "au carré vaut", x * x)

```

<!-- #region -->
Pour la lancer, on utilise la commande `streamlit` :

```bash
streamlit run apps/slider.py
```
<!-- #endregion -->

<small>Comme les fois précédentes, les cellules qui lancent les API dans ce notebook ne sont pas
exécutables, entrez-les dans votre terminal.</small>


L'application est alors servi depuis votre machine et un onglet s'ouvre dans votre navigateur (sinon
allez à l'URL donnée dans la console).


Comment ça marche ? Eh bien à chaque fois que vous intergissez avec le slider, Streamlit relance le
script, en injectant la nouvelle valeur.


Il existe [de nombreux widgets](https://docs.streamlit.io/library/api-reference) prédéfinis, mais le
principe est toujours le même : à chaque interaction on recharge tout en injectant les bonnes
valeurs. Ça rend les applications Streamlit plutôt simples à comprendre, mais ça oblige à faire pas
mal de pirouette pour que les interactions soient fluides. Notamment, on se repose énormément sur
des mécanismes de mise en cache.

## Mise en cache

Voici par exemple comment afficher un `Dataframe` pandas récupéré depuis un CSV distant en ne le
retéléchargeant pas à chaque modification :

```python
# %load apps/show_dataframe.py
import pandas as pd
import streamlit as st


# Le décorateur `st.cache` permet de conserver le résultat de la fonction d'un chargement sur l'autre
# ainsi on n'ira chercher ces données qu'une seule fois
@st.cache
def get_data():
    url = "http://data.insideairbnb.com/france/ile-de-france/paris/2021-09-09/visualisations/listings.csv"
    return pd.read_csv(url)


df = get_data()


st.title("Listings AirBnB pour Paris")
st.markdown(
    "Cette page présente les statistiques du groupe [Inside AirBnB](http://data.insideairbnb.com) pour Paris"
)

st.dataframe(df)

```

<!-- #region -->
```bash
streamlit run apps/show_dataframe.py
```
<!-- #endregion -->

Voir [la doc](https://docs.streamlit.io/library/advanced-features/caching) pour les détails de fonctionnement de `st.cache`.


## Widgets graphiques

On peut facilement afficher des graphiques, ici par exemple des histogrammes

```python
# %load apps/graphs.py
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


@st.cache
def get_data():
    url = "http://data.insideairbnb.com/france/ile-de-france/paris/2021-09-09/visualisations/listings.csv"
    df = pd.read_csv(url)
    # On vire les données foireuses
    return df[df["price"] > 20]


df = get_data()


st.title("Listings AirBnB pour Paris")
st.markdown(
    "Cette page présente les statistiques du groupe [Inside AirBnB](http://data.insideairbnb.com) pour Paris"
)

st.subheader("Répartition des prix")

fig, ax = plt.subplots()

ax.hist(df["price"], bins="auto")

st.pyplot(fig)


st.subheader("Répartition des nombres de reviews")

fig, ax = plt.subplots()

ax.hist(df["number_of_reviews"], bins="auto")

st.pyplot(fig)

st.subheader("Détails complets")

st.dataframe(df)
```

<!-- #region -->
```bash
streamlit run apps/graphs.py
```
<!-- #endregion -->

Mais aussi des trucs plus rigolos comme des cartes

```python
# %load apps/map.py
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


@st.cache
def get_data():
    url = "http://data.insideairbnb.com/france/ile-de-france/paris/2021-09-09/visualisations/listings.csv"
    df = pd.read_csv(url)
    # On vire les données foireuses
    return df[df["price"] > 20]


df = get_data()


st.title("Listings AirBnB pour Paris")
st.markdown(
    "Cette page présente les statistiques du groupe [Inside AirBnB](http://data.insideairbnb.com) pour Paris"
)

st.subheader("Carte de listings à plus de 1000 € la nuit")

# Ça marche parce que le dataframe contient des colonnes `latitude` et `longitude``
st.map(df[df["price"] > 1000])

st.subheader("Détails complets")

st.dataframe(df)
```

<!-- #region -->
```bash
streamlit run apps/map.py
```
<!-- #endregion -->

## Communication entre widgets

Les widgets communiquent aussi entre eux, on peut par exemple utiliser un slider pour sélectionner une fourchette de prix

```python
# %load apps/map_and_slider.py
import pandas as pd
import streamlit as st


@st.cache
def get_data():
    url = "http://data.insideairbnb.com/france/ile-de-france/paris/2021-09-09/visualisations/listings.csv"
    df = pd.read_csv(url)
    # On vire les données foireuses
    return df[df["price"] > 20]


df = get_data()


st.title("Listings AirBnB pour Paris")
st.markdown(
    "Cette page présente les statistiques du groupe [Inside AirBnB](http://data.insideairbnb.com) pour Paris"
)

st.subheader("Carte des listings")

absolute_min_price = df["price"].min().astype(float).item()
absolute_max_price = df["price"].max().astype(float).item()

min_price, max_price = st.slider(
    "min_price",
    absolute_min_price,
    absolute_max_price,
    value=(
        df["price"].min().astype(float).item(),
        (absolute_min_price + absolute_max_price) / 2,
    ),
    step=10.0,
)

st.map(df[df["price"].between(min_price, max_price)])

st.subheader("Détails complets")

st.dataframe(df)

```

<!-- #region -->
```bash
streamlit run apps/map_and_slider.py
```
<!-- #endregion -->
