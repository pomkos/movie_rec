import pandas as pd
import streamlit as st
import app.helpers as h
import app.engine as e

st.title("Movie Recommendations")


def app():
    movies = pd.read_csv("data/movies.csv")
    ratings = pd.read_csv("data/ratings.csv")
    movies['cleaned_title'] = movies['title'].apply(h.clean_title)
    
    search_term = st.text_input()