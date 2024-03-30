import numpy as np
import pandas as pd
import pickle

def load_corr_matrix_from_pickle(file_path):
    with open(file_path, 'rb') as f:
        corr_matrix = pickle.load(f)
    return corr_matrix

# Load the correlation matrix from the Pickle file
corr_matrix = load_corr_matrix_from_pickle(r'..\\database\\correlation_matrix.pkl')

def get_similar(movie_name, rating, corr_matrix):
    similar_score = corr_matrix[movie_name] * (rating - 2.5)
    similar_score = similar_score.sort_values(ascending=False)
    return similar_score

def get_similar_movies(movie_names, user_ratings, corr_matrix):
    similar_movies_list = []
    for i, (movie_name, rating) in enumerate(zip(movie_names, user_ratings)):
        similar_movies = get_similar(movie_name, rating, corr_matrix).head(10)
        similar_movies_list.append(similar_movies.index.tolist())  # Append only movie titles
    return similar_movies_list
