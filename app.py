import streamlit as st
import pickle
import pandas as pd
import requests

# Page config (Netflix style wide layout)
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Custom CSS (Netflix UI)
st.markdown("""
<style>
body {
    background-color: #0b0c10;
}
.title {
    font-size: 48px;
    font-weight: bold;
    color: #e50914;
    text-align: center;
}
.card {
    background-color: #141414;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    transition: transform 0.3s;
}
.card:hover {
    transform: scale(1.05);
}
.movie-title {
    color: white;
    font-size: 14px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# Load data
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Fetch poster (OMDb)
def fetch_poster(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey=2c176e62"
    data = requests.get(url).json()

    if data.get('Response') == 'True' and data.get('Poster') != 'N/A':
        return data.get('Poster')
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names = []
    posters = []

    for i in movie_list:
        title = movies.iloc[i[0]].title
        names.append(title)
        posters.append(fetch_poster(title))

    return names, posters

# Title
st.markdown('<div class="title">🎬 AI Movie Recommender</div>', unsafe_allow_html=True)

# Dropdown
selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

# Button
if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.image(posters[i], use_container_width=True)
            st.markdown(f'<div class="movie-title">{names[i][:30]}...</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)