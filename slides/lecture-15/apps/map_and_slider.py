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
