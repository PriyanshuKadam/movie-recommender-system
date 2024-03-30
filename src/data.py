import pandas as pd
import sqlite3

# Load data into pandas DataFrames
ratings = pd.read_csv(r'../MOVIE-RECOMMENDER-SYSTEM/input/ratings_small.csv').drop('timestamp', axis=1)

movies = pd.read_csv(r'../MOVIE-RECOMMENDER-SYSTEM/input/movies.csv')

pattern = r'^(?P<name>.+)\s\((?P<year>\d{4})\)$'
movies[['movie_name', 'year']] = movies['title'].str.extract(pattern)
movies['title'] = movies['movie_name']
movies['genres'] = movies['genres'].str.replace('|', ', ')

links = pd.read_csv(r'../MOVIE-RECOMMENDER-SYSTEM/input/links.csv').drop('imdbId', axis=1)
movies = pd.merge(movies, links, on='movieId')
movies = movies.drop_duplicates(subset=['title'])
movies = movies.drop_duplicates(subset=['tmdbId'])

# Remove missing values from movies DataFrame
movies.dropna(inplace=True)

# Convert 'tmdbId' column to integers
movies['tmdbId'] = movies['tmdbId'].astype(int)

# Connect to SQLite database
conn = sqlite3.connect(r'../MOVIE-RECOMMENDER-SYSTEM/database/data.db')

# Write DataFrames to SQLite tables
ratings.to_sql('ratings', conn, if_exists='replace', index=False)
movies.to_sql('movies', conn, if_exists='replace', index=False)

# Commit and close connection
conn.commit()
conn.close()