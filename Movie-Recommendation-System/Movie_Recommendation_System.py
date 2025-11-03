import os
import requests
from pathlib import Path
import zipfile
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer


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
