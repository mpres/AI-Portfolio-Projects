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
