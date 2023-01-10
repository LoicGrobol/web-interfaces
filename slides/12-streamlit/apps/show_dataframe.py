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
