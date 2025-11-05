def prep_movies(movies_df: pd.DataFrame, ratings_df: pd.DataFrame) -> pd.DataFrame:
  ''' Parameters: 1. 'movies_df' is a raw data frame
                  2. 'ratings_df' is a raw dta frame
      Returns:    1. returns a processed and encoded dataframe ready for SVD algo
      
      Outline:    1. merge the dataframes (movies and ratings)
                  2. encode ids
                  3. create encoder objects and multi-label-binarizer

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


  return df



