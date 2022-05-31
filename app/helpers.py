import re
import pandas as pd
import sqlalchemy as sq
from typing import List, Literal

def clean_title(title: str) -> str:
    '''
    Keeps only letters, numbers, whitespaces. 
    Replaces everything else with nothing.
    '''
    return re.sub("[^a-zA-Z0-9 ]", "", title)


def save_data(dataset: pd.DataFrame, table_name: str, if_exists: str = 'fail', index: bool = False) -> bool:
    '''
    Saves dataframe to the movie_data sqlite database
    '''
    engine = sq.create_engine("sqlite:///data/movie_data.sql")
    try:
        with engine.connect() as cnx:
            dataset.to_sql(name=table_name, con=cnx, if_exists=if_exists, index=index)
            return True
    except:
        print("Does this table already exist in movie_data.sql?")
        return False


def load_data(table_name: str) -> pd.DataFrame:
    '''
    Loads table from the movie_data sqlite database
    '''
    engine = sq.create_engine("sqlite:///data/movie_data.sql")
    with engine.connect() as cnx:
        return pd.read_sql(table_name, cnx)


def check_genre_exists(value: str, genre_list: List[str], use_all_genres: bool) -> bool:
    '''
    Returns true if any genre from list is also in the given string.
    '''
    bool_list = [True if genre in value else False for genre in genre_list]
    num_trues = sum(bool_list)
    if (num_trues > 0) & (use_all_genres==False):
        return True
    elif (num_trues == len(genre_list)) & (use_all_genres):
        return True
    else: 
        return False


def find_unique_genres(movies: pd.DataFrame) -> List[str]:
    movies['genres_split'] = movies['genres'].apply(lambda x: x.split('|'))

    unique_genres = []
    for genre_list in movies['genres_split']:
        for genre in genre_list:
            if genre not in unique_genres:
                unique_genres.append(genre)
    if '(no genres listed)' in unique_genres:
        unique_genres.remove('(no genres listed)')
    elif 'None' in unique_genres:
        unique_genres.remove('None')

    unique_genres.sort()
    return unique_genres