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