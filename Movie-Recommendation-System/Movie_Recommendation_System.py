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


def explore_dir(path):
  """ This would explore the directory and return the outline of it """
  for dir_path, dir_names, file_names in os.walk(path):
    print(f"Directory count {len(dir_names)}, movies count {len(file_names)} in '{file_names}'")


### 10/31/25 grab files and merge them into a useful structure, one file using pandas

movies_df = pd.read_csv('data/ml-latest-small/movies.csv')
tags_df = pd.read_csv('data/ml-latest-small/tags.csv')
rating_df = pd.read_csv('data/ml-latest-small/ratings.csv')
links_df = pd.read_csv('data/ml-latest-small/ratings.csv')

#merge files
df = pd.merge(rating_df,movies_df[['movieId','genres']], on = 'movieId', how = 'left')

#create encoder for user and movies
le = LabelEncoder()
df['movieId'] = le.fit_transform(df['movieId'])
df['userId'] = le.fit_transform(df['userId'])

#add user and movie encoders
user_encoder = LabelEncoder()
movie_encoder = LabelEncoder()
#create multiLabelBinarizer
mlb = MultiLabelBinarizer()

# create list of genres via the "|", and take out the old genres field
genres_list = df.pop('genres').str.split('|')

#create MLB data 
MLB_data = mlb.fit_transform(genres_list)
#create MLB data frame
MLB_df = pd.DataFrame(MLB_data,columns=mlb.classes_, index = df.index)
# join MLB to main data frame by the 
df = df.join(MLB_df)
# clean data frame, pop
df = df.drop('(no genres listed)', axis=1)

#Train Test Split
train_df, test_df = train_test_split(df,test_size=.2,train_size=.8)

#Get reader,data and trainset
reader = Reader(rating_scale = (0.5,5))
data = Dataset.load_from_df(train_df[['userId','movieId','rating']],reader )
train_set = data.build_full_trainset()

#Create model svc
model_svd = SVD()
model_svd.fit(train_set)

prediction_svd = model_svd.test(train_set.build_anti_testset())
accuracy.rmse(prediction_svd)


#create function to get top movie recommendations

def get_best_n_recommendations(user_id: str, n: int = 5):
  ''' user_id will represent a type string and will be an id found in the
      user_df
      n is a "int" type and will return the amount recommendations returned
  '''
  # Get the amount of movies this user has seenmovies this user has seen
  user_movies = df[df['userId'] == user_id]['movieID'].unique()
  # return all the movies minus the ones' this user has seen
  all_movies = df['movie.'].unqiue()
  movies_to_predict = list(set(all_movies) - set(user_movies))
  # use the model to return the amount of movies to see
  user_movie_pairs = [(user_id,movie_id, 0) for movie_id in movies_to_predict]
  predictions_cf = model_svd.test(user_movie_pairs)

  top_n_recommendations = sorted(predictions_cf, key = lambda x: x.est, reverse = True)[:n]

  top_n_movie_ids = [int(pred.ii) for pred in top_n_recommendations]

  top_n_movies = movie_encoder.inverse_transform(top_n_movie_ids)
  
  return top_n_movies
