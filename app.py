import pickle
import gzip
import streamlit as st
import requests
import pandas as pd
import os

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    
    if "poster_path" in data and data["poster_path"]:
        return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    return "https://via.placeholder.com/500"  # Placeholder image if poster is missing

# Function to recommend movies
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error("Movie not found in dataset.")
        return [], []

    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommend_poster_movie = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommend_poster_movie.append(fetch_poster(movie_id))  

    return recommended_movies, recommend_poster_movie


# Streamlit UI
st.title("🎬 Movie Recommendation System")

# Load movies dataframe
if os.path.exists("movie_dict.pkl"):
    with open("movie_dict.pkl", "rb") as f:
        movie = pickle.load(f)
    movies = pd.DataFrame(movie)
else:
    st.error("Error: `movie_dict.pkl` file not found.")
    st.stop()

# Load similarity matrix (compressed version)
similarity_file = "similarity.pkl.gz"

if os.path.exists(similarity_file):
    with gzip.open(similarity_file, "rb") as f:
        similarity = pickle.load(f)  # Correct way to load pickled data
else:
    st.error("Error: `similarity.pkl.gz` file not found.")
    st.stop()

# Movie selection dropdown
selected_movie_name = st.selectbox("Select a Movie", movies['title'].values)

if st.button("Recommend"):
    name, poster = recommend(selected_movie_name)

    # Show recommended movies with posters
    cols = st.columns(5, gap="large")
    for idx, col in enumerate(cols):
        if idx < len(name):  
            col.image(poster[idx], caption=name[idx])

st.caption("Made with ❤️ by :red[_Suraj Yadav_] 😎")

