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

st.subheader("Carte des listings")

min_price = st.slider(
    "min_price",
    df["price"].min().astype(float).item(),
    1000.0,
    value=(df["price"].min().astype(float).item(), 100.0),
    step=10.0,
)

st.map(df[df["price"] > min_price])

st.subheader("Détails complets")

st.dataframe(df)
