import os
import requests
from pathlib import Path
from surprise import Dataset, Reader
from surprise.prediction_algorithms.matrix_factorization import SVD
from surprise import accuracy
import zipfile
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.model_selection import train_test_split
import time


def prep_movies(movies_df: pd.DataFrame, ratings_df: pd.DataFrame) -> pd.DataFrame:
  ''' Parameters: 1. 'movies_df' is a raw data frame
                  2. 'ratings_df' is a raw dta frame
      Returns:    1. returns a processed and encoded dataframe ready for SVD algo

      Outline:    1. merge the dataframes (movies and ratings)
                  2. encode ids
                  3. create encoder objects and multi-label-binarizer
                  4. fit label encoders, process "|" column
                  5. Process MLB
                  6. return processed df


  '''
  df = pd.merge(rating_df,movies_df[['movieId','genres']], on = 'movieId', how = 'left')

  #create encoder for movieId and userId
  le = LabelEncoder()
  df['movieId'] = le.fit_transform(df['movieId'])
  df['userId'] = le.fit_transform(df['userId'])

  #merge files

  #2 add user and movie encoders
  user_encoder = LabelEncoder()
  movie_encoder = LabelEncoder()

  #3 create multiLabelBinarizer
  mlb = MultiLabelBinarizer()

  #4 fit label encoders
  df['userId'] = user_encoder.fit_transform(df['userId'])
  df['movieId'] = movie_encoder.fit_transform(df['movieId'])
  # create list of genres via the "|", and take out the old genres field
  genres_list = df.pop('genres').str.split('|')

  #5, create MLB data
  MLB_data = mlb.fit_transform(genres_list)
  #create MLB data frame
  MLB_df = pd.DataFrame(MLB_data,columns=mlb.classes_, index = df.index)
  # join MLB to main data frame by the
  df = df.join(MLB_df)
  # clean data frame, pop
  df = df.drop('(no genres listed)', axis=1)

  return df

#11/5/25, depends

def explore_dir(path):
  """ This would explore the directory and return the outline of it """
  for dir_path, dir_names, file_names in os.walk(path):
    print(f"Directory count {len(dir_names)}, movies count {len(file_names)} in '{file_names}'")


# 11/5/25
def get_best_n_recommendations(df: pd.DataFrame, user_id: str, n: int = 5):
  ''' Parameters: 1. df needs to be a processed.
                  2. user_id will represent a type string and will be an id found in the
                    user_df
                  3. n is a "int" type and will return the amount recommendations returned

  '''
  # Get the amount of movies this user has
  user_movies = df[df['userId'] == user_id]['movieId'].unique()
  # return all the movies minus the ones' this user has seen
  all_movies = df['movieId'].unique()

  movies_to_predict = list(set(all_movies) - set(user_movies))
  # use the model to return the amount of movies to see
  user_movie_pairs = [(user_id,movie_id, 0) for movie_id in movies_to_predict]

  predictions_cf = model_svd.test(user_movie_pairs)

  top_n_recommendations = sorted(predictions_cf, key = lambda x: x.est, reverse = True)[:n]

  top_n_movie_ids = [int(pred.iid) for pred in top_n_recommendations]

  top_n_movies = movie_encoder.inverse_transform(top_n_movie_ids)

  return top_n_movies


def get_titles(movie_df: pd.DataFrame,ids: list) -> list:
  '''
  This function will return a list of titles from a list of ids

  args:
    movie_df = a data frame of movie ids with their titles
    ids = this should be a list of movies ids you want the title to
  results:
    returns movies titles
  '''
  try:

    assert 'movieId' in movie_df.columns
    assert 'title' in movie_df.columns
    return movies_df[movies_df['movieId'].isin(ids)]



  except Exception as e:
    print(f'An error occurred')

  return ""

#added create_new_user function for gradio 11/17/25
def create_new_user(df: pd.DataFrame, new_user_id: int, user_movie_scores: list[tuple[int,float]] ) -> pd.DataFrame:
  '''
    purpose:
            This function will take in a new_user_id, a dataframe and user_movie_scores
             It will return return a new dataframe that represent an instance of one movie review for that user.
             This function will be used for a gradio setup
    outline:
            validate data types, make sure df argument has the right columns. make usre new_user_is is unique to df
            Loop through user_movie_socres, grab genre informatiob from movie id, create entry row for each loop iteration.
            return new rows of data.

    args:
        df - this is a dataframe where we get the genre information about the movies entered.
        new_user_id - this will be a new user_id that is unique to the df frame colum user_Id.
        user_movie_scores - this should be a list of tuples, the first value is the movie_Id the second is a rating of 0.0 - 5.0 the increment of .5
    return:
        returns rows in the same format as rows in the df pandas data frame.

  '''

  #Validate inputs

  if not isinstance(df, pd.DataFrame):
    raise TypeError("Input 'df' must be a pandas data frame")

  if not isinstance(new_user_id, int):
    raise TypeError("Input 'new_user_id' must be an int")

  if not isinstance(user_movie_scores, list):
    raise TypeError("Input 'user_movie_scores' must be a list of tuples with an int,float")

  #Validate make sure df has user a column user

  if not 'userId' in df.columns:
    raise Exception("the 'userId' column is not in DataFrame 'df'")

  if new_user_id in set(df['userId']):
    raise Exception(f" the new_user_id {new_user_id} is not unique")

  for movie_pair in user_movie_scores:
    if not movie_pair[0] in list(df['movieId']):
      raise Exception(f"the movie id {movie_pair[0]} is not found in the data frame 'df'")
    if movie_pair[1] > 5 or movie_pair[1] < 0:
      raise Exception(f"the movie rating {movie_pair[1]} for movie id {movie_pair[0]} must be between 0 and 5")

  #capture current df into df_result 11/17/25
  df_result = df.copy(deep=True)

  #Loop through the user_movie_scores

  for movie_pair in user_movie_scores:
    row = df[df['movieId'] == movie_pair[0]].iloc[0:1]
    row[['userId','rating','timestamp']] = new_user_id, movie_pair[1], time.time()
    df_result = pd.concat([df_result,row], ignore_index=True)
    

  return df_result
