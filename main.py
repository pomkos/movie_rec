from enum import unique
import pandas as pd
import streamlit as st
from app import helpers as h
from app import engine as e
from typing import Tuple, List


st.title("Movie Recommendation App")
@st.cache
def load_ratings_dataset() -> pd.DataFrame:
    '''
    Created solely so that the dataset isn't loaded each time on
    page refresh
    '''
    return pd.read_csv("data/ratings.csv")


def get_user_input(movies_df: pd.DataFrame) -> Tuple[str, list, bool]:
    ph = st.container()
    with st.form('user_input'):
        user_term = st.text_input("Search for a movie", 
                                  value='toy story', 
                                  help='We will base our recommendations off of this movie').title()
        unique_genres = h.find_unique_genres(movies_df)
        unique_genres = ["Any genre is fine"] + unique_genres
        user_genre_list = st.multiselect("What genres would you like to watch?", 
                                         options=unique_genres, 
                                         default='Any genre is fine',
                                         help='Find movies that belong to any or all of these genres')
        
        use_all_genres = st.checkbox("Resulting movies should belong to all selected genres", 
                                     help='If unchecked, will recommend movies that belong to at least one of the selected genres')
        submit = st.form_submit_button('Submit')

    if "Any genre is fine" in user_genre_list:
        user_genre_list = unique_genres

    if not submit:
        ph.info("Search for a movie title to get recommendations based on what similar users liked!")
        st.stop()
    
    return user_term, user_genre_list, use_all_genres

def app():
    movies = h.load_data('movies')
    movies['cleaned_title'] = movies['title'].apply(h.clean_title)
    
    user_term, user_genre_list, use_all_genres = get_user_input(movies)
    
    search_results = e.search(user_term, movies)
    movie_title_similar_to_search_term = search_results.iloc[0, 1] # the title that we found in db based on search term, for user info only
    movie_id = search_results.iloc[0,0] # user's movieId, used to find similar movies

    st.info("The movie we found using your search term:")
    st.write(search_results.head(1)[['cleaned_title', 'genres', 'similarity']])

    ratings = load_ratings_dataset()    
    results = e.find_similar_movies(movies, ratings, movie_id)

    show_results(results, movies, ratings, movie_title_similar_to_search_term, user_genre_list, use_all_genres)


def show_results(results: pd.DataFrame, all_movies: pd.DataFrame, ratings: pd.DataFrame, \
                 movie_title: str, user_genre_list: List[str], use_all_genres: bool):
    '''
    Function to easily find and format results for presenting to user
    '''
    if results.empty:
        # if no results, then show a random sample of all movies that fit the genre
        all_movies = all_movies[all_movies['genres'].apply(h.check_genre_exists, genre_list=user_genre_list, use_all_genres=use_all_genres)]
        results = all_movies.sample(10)
        results = results[['title', 'genres']]
        st.info("No similar movies found but here's a random sample of movies that belong to your chosen genres")

    else:
        # filter by user's preferred genre(s)
        results = results[results['genres'].apply(h.check_genre_exists, genre_list=user_genre_list, use_all_genres=use_all_genres)]
        st.success(f"Recommendations for you that are similar to {movie_title}")

    if use_all_genres == False:
        results['genres'] = results['genres'].apply(h.extract_string, terms_to_extract=user_genre_list)
    
    results = h.add_average_ratings_col(results, ratings).drop('movieId', axis=1)
    st.table(results.set_index('title')[['genres', 'avg_rating', 'score']])

if __name__ == "__main__":
    app()