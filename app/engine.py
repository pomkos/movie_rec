import pandas as pd
import numpy as np

from app import helpers as h

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def search(title: str, movies: pd.DataFrame) -> pd.DataFrame:
    '''
    Turns search term into a vector, resulting top 5 results
    '''
    # ngrams: number of words to search for together
    # ex: Toy Story 1995: "toy", "story", "1995"; "toy story", "story 1995"

    vectorizer = TfidfVectorizer(ngram_range=(1,2))
    tfidf = vectorizer.fit_transform(movies['cleaned_title'])

    title = h.clean_title(title)
    query_vec = vectorizer.transform([title])
    # returns how similar search title is to each title
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    # find the 5 most similar titles by idx, in asc order
    # kinda like df['col'].sort_values(ascending=False).loc[:-5]
    indices = np.argpartition(similarity, -5)[-5:]
    movies['similarity'] = similarity
    results = movies.iloc[indices].sort_values('similarity', ascending=False) # return with most similar up top
    return results

def find_similar_users_movies(ratings_df: pd.DataFrame, movie_id: int, high_rating: int):
    # find the users that liked the movie being searched for
    similar_users = ratings_df[(ratings_df["movieId"] == movie_id) & (ratings_df['rating']>=high_rating)]['userId'].unique()

    # find the movies that similar users liked
    similar_user_recs = ratings_df[(ratings_df['userId'].isin(similar_users)) & (ratings_df['rating']>=high_rating)]['movieId']

    # find the top 10% of movies
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)
    similar_user_recs = similar_user_recs[similar_user_recs > 0.1]

    return similar_user_recs

def find_similar_movies(movies: pd.DataFrame, ratings: pd.DataFrame, movie_id: int, high_rating: int = 4) -> pd.DataFrame:
    similar_user_recs = find_similar_users_movies(ratings, movie_id, high_rating)
    
    # all users who watched the movie recommended to us
    all_users_who_watched_movie = ratings[(ratings['movieId'].isin(similar_user_recs.index))]
    all_user_recs = all_users_who_watched_movie['movieId'].value_counts()/len(all_users_who_watched_movie['userId'].unique())
    
    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ['similar_ppl','all_ppl']

    # score = ratio of similar:avg users who liked movie
    rec_percentages['score'] = rec_percentages['similar_ppl'] / rec_percentages['all_ppl']
    rec_percentages = rec_percentages.sort_values('score', ascending=False)
    
    # left_index is the movieId
    return rec_percentages.head(10).merge(movies, left_index=True, right_on='movieId')[['movieId', 'score','title','genres']]