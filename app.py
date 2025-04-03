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
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #FF5733;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("🔍 Search & Discover")
st.sidebar.subheader("Features")
st.sidebar.write("✅ Search movies")
st.sidebar.write("✅ Get personalized recommendations")
st.sidebar.write("✅ View all movies in the database")
st.sidebar.write("✅ Learn about this app")
st.sidebar.write("📩 Contact: suraj@example.com")

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

# Tabs for better UI
tabs = st.tabs(["🔍 Search & Recommend", "📜 All Movies", "🌟 Top Rated", "ℹ️ About"])

with tabs[0]:
    st.subheader("🔍 Movie Recommendation")
    title_search = st.text_input("Search Movie Title")
    filtered_movies = movies[movies['title'].str.contains(title_search, case=False, na=False)] if title_search else movies
    selected_movie_name = st.selectbox("Select a Movie", filtered_movies['title'].values)
    
    if st.button("Recommend 🎥"):
        name, poster = recommend(selected_movie_name)
        st.subheader(f"Top 5 Recommendations for {selected_movie_name}:")
        cols = st.columns(5, gap="large")
        for idx, col in enumerate(cols):
            if idx < len(name):  
                col.image(poster[idx], caption=name[idx], use_container_width=True)

with tabs[1]:
    st.subheader("📜 All Available Movies")
    if 'title' in movies.columns:
        st.dataframe(movies[['title']], use_container_width=True)
    else:
        st.error("Error: Expected columns not found in dataset.")

with tabs[2]:
    st.subheader("🌟 Top Rated Movies")
    if 'title' in movies.columns and 'rating' in movies.columns:
        top_movies = movies.sort_values(by='rating', ascending=False).head(10)
        st.dataframe(top_movies[['title', 'rating']], use_container_width=True)
    else:
        st.error("Error: Rating column not found.")

with tabs[3]:
    st.subheader("ℹ️ About the App")
    st.markdown(
        """
        Welcome to the **Movie Recommendation System**! 🎬 This app allows you to:
        - Search for movies 🎥
        - Get top 5 recommendations based on similarity 🔍
        - Browse all available movies 📜
        - View the top-rated movies 🌟
        - Enjoy an interactive and easy-to-use UI 😎
        
        **Made with ❤️ by Suraj Yadav**
        """
    )

st.caption("Made with ❤️ by :red[_Suraj Yadav_] 😎")
