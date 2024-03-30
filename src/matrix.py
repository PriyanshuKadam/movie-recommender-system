import numpy as np
import pandas as pd
import sqlite3
import pickle

# Connect to SQLite databases
con = sqlite3.connect(r'../MOVIE-RECOMMENDER-SYSTEM/database/data.db')

# Load data from SQLite tables
ratings_query = "SELECT movieId, userId, rating FROM ratings"
movies_query = "SELECT movieId, title, year, genres, tmdbId FROM movies"

ratings = pd.read_sql(ratings_query, con)
movies = pd.read_sql(movies_query, con)

# Merge ratings with movie names
ratings_with_name = pd.merge(ratings, movies, on='movieId')

# Create pivot table for user-movie ratings
movies_users = pd.pivot_table(ratings_with_name, index='userId', columns='title', values='rating', fill_value=0)

# Compute correlation matrix
corr_matrix = movies_users.corr(method='pearson')

# Save correlation matrix to a Pickle file
with open(r'../MOVIE-RECOMMENDER-SYSTEM/database/correlation_matrix.pkl', 'wb') as f:
    pickle.dump(corr_matrix, f)

# Close connection
con.close()