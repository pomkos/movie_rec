import re
import pandas as pd
import sqlalchemy as sq

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