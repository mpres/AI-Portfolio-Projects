
# 10/30/25,
# 1. Get the datasource
# 2. unzip the data source
# 3. Explore the datasource


import requests
from pathlib import Path
import zipfile

#Create directories
data_path = Path("data/")
movie_path = data_path / "movie_data"

if movie_path.is_dir():
  print("Directory Movie Path is already created")
else:
  print(f"Creating Directory {movie_path} " )
  movie_path.mkdir(parents=True,exist_ok=True)

# url to dataset

url_path = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"

with open(movie_path / "small_movie_data.zip", 'wb' ) as f:
  request = requests.get(url_path)
  print("Downloading Movie Data set")
  f.write(request.content)

# Now let's unpack this data set

with zipfile.ZipFile(movie_path / "small_movie_data.zip", 'r') as zip_ref:
  print("unzipping file")
  zip_ref.extractall(movie_path)

