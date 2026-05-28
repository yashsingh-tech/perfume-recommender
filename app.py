import streamlit as st
import pandas as pd
import pickle as pkl

## similarity code 
similarity = pkl.load(open("similarity.pkl", "rb"))
df = pkl.load(open("perfume_df.pkl","rb"))

df['short_title'] = df['brand'] + " " + df['title'].str.split().str[:2].str.join(" ")


# Title
st.set_page_config(
    page_title="Luxury Perfume AI",
    page_icon="🌸",
    layout="centered"
)

st.markdown(
    """
    <h1 style='text-align: center; color: #ff4b4b;'>
    🌸 Luxury Perfume Recommender
    </h1>
    """,
    unsafe_allow_html=True
)

st.write("### Discover fragrances you'll love ✨")



## recommendation funcation 

def recommend_perfume(perfume_name):

    perfume_name = perfume_name.lower()

    matches = df[df['short_title'].str.lower() == perfume_name]

    if matches.empty:
        return ["Perfume not found"]

    idx = matches.index[0]

    distances = similarity[idx]

    perfume_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for i in perfume_list:
        recommendations.append(df.iloc[i[0]]['short_title'])

    return recommendations


# Dropdown
selected_perfume = st.selectbox(
    "Choose a perfume",
    df['short_title'].values
)

# Button
if st.button("Recommend"):

    results = recommend_perfume(selected_perfume)

    st.subheader("Recommended Perfumes")

    for perfume in results:
        st.write("✨", perfume)
