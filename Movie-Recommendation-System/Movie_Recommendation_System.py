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
