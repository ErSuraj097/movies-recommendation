import pickle
import gzip
import streamlit as st
import requests
import pandas as pd

# ✅ Load the compressed similarity file
try:
    with gzip.open("similarity.pkl.gz", "rb") as f:
        similarity = pickle.load(f)
    st.success("✅ Successfully loaded similarity.pkl.gz!")
except Exception as e:
    st.error(f"❌ Error loading similarity.pkl.gz: {e}")
    similarity = None  # Prevent further errors

# ✅ Load the movie dictionary
try:
    movie = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movie)
    st.success("✅ Successfully loaded movie_dict.pkl!")
except Exception as e:
    st.error(f"❌ Error loading movie_dict.pkl: {e}")
    movies = None

# ✅ Function to fetch movie poster
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path', None)
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500"  # Default placeholder image
    except Exception as e:
        st.error(f"❌ Error fetching poster: {e}")
        return "https://via.placeholder.com/500"

# ✅ Function to recommend movies
def recommend(movie_name):
    try:
        index = movies[movies['title'] == movie_name].index[0]
        distances = similarity[index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        recommended_posters = []
        
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_posters.append(fetch_poster(movie_id))
        
        return recommended_movies, recommended_posters
    except Exception as e:
        st.error(f"❌ Error in recommendation system: {e}")
        return [], []

# ✅ Streamlit UI
st.title("🎬 Movie Recommendation System")

if movies is not None:
    selected_movie_name = st.selectbox("Choose a movie:", movies['title'].values)

    if st.button('🎥 Recommend Movies'):
        if similarity is not None:
            names, posters = recommend(selected_movie_name)

            if names:
                cols = st.columns(5)
                for col, name, poster in zip(cols, names, posters):
                    with col:
                        st.image(poster, caption=name)
            else:
                st.warning("⚠️ No recommendations found!")
        else:
            st.error("⚠️ Similarity matrix not loaded!")

st.caption('💙 Made with ❤️ by **Suraj Yadav**')
