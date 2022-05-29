import pandas as pd
import streamlit as st
from app import helpers as h
from app import engine as e


st.title("Movie Recommendations")
@st.cache
def load_ratings_dataset() -> pd.DataFrame:
    '''
    Created solely so that the dataset isn't loaded each time on
    page refresh
    '''
    return pd.read_csv("data/ratings.csv")

def app():
    movies = h.load_data('movies')
    ratings = load_ratings_dataset()
    movies['cleaned_title'] = movies['title'].apply(h.clean_title)
    
    search_term = st.text_input("Search for a movie", value='toy story').title()

    if not search_term:
        st.info("Search for a movie title to get recommendations based on what similar users liked!")
        st.stop()
    
    movie_id = e.search(search_term, movies).iloc[0,0]
    results = e.find_similar_movies(movies, ratings, movie_id)
    st.success(f"Recommendations for you that are similar to {search_term}")
    st.table(results)

if __name__ == "__main__":
    app()