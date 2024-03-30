import pandas as pd
import sqlite3
import streamlit as st
import requests
from train import get_similar_movies, load_corr_matrix_from_pickle

# Connect to SQLite database
conn = sqlite3.connect('../database/data.db')

# Load data from SQLite tables
ratings_query = "SELECT movieId, userId, rating FROM ratings"
movies_query = "SELECT movieId, title, year, genres, tmdbId FROM movies"

ratings = pd.read_sql(ratings_query, conn)
movies = pd.read_sql(movies_query, conn)

# Merge ratings with movie names
ratings_with_name = pd.merge(ratings, movies, on='movieId')

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def get_details(movie_title):
    movie_row = movies[movies['title'] == movie_title]
    return movie_row['genres'].iloc[0], movie_row['year'].iloc[0], movie_row['tmdbId'].iloc[0]

st.title('Movie Recommender System')

# Initialize empty list to store selected movies
selected_movies = []

# Allow user to select multiple movies
movie_options = movies['title'].values
selected_movies = st.multiselect('Search and select movies', movie_options)

# Load the correlation matrix
corr_matrix = load_corr_matrix_from_pickle(r'..\\database\\correlation_matrix.pkl')

# Initialize list to store movie ratings
user_movie_ratings = []

if len(selected_movies) > 0:
    # Display details for each selected movie
    for i in range(0, len(selected_movies), 2):
        # Create a row layout for two movies
        col1, col2 = st.columns(2)

        with col1:
            if i < len(selected_movies):
                movie_title_1 = selected_movies[i]
                genre_1, year_1, movie_id_1 = get_details(movie_title_1)
                st.subheader(movie_title_1)
                st.image(fetch_poster(movie_id_1), width=200)
                st.write('Genre: ', genre_1)
                st.write('Year: ', year_1)
                rating_1 = st.slider(f"Rate {movie_title_1} (1-5)", 1, 5, key=f"rating_{movie_title_1}")
                user_movie_ratings.append((movie_title_1, rating_1))  # Append rating to list

        with col2:
            if i + 1 < len(selected_movies):
                movie_title_2 = selected_movies[i + 1]
                genre_2, year_2, movie_id_2 = get_details(movie_title_2)
                st.subheader(movie_title_2)
                st.image(fetch_poster(movie_id_2), width=200)
                st.write('Genre: ', genre_2)
                st.write('Year: ', year_2)
                rating_2 = st.slider(f"Rate {movie_title_2} (1-5)", 1, 5, key=f"rating_{movie_title_2}")
                user_movie_ratings.append((movie_title_2, rating_2))  # Append rating to list

# Add a button to save the ratings
if st.button('Recommend'):
    st.write("Movie Ratings Saved Successfully!")

    # Call recommendation function
    # Extract movie names and ratings from user_movie_ratings list of tuples
    movies_selected = [movie for movie, _ in user_movie_ratings]
    ratings_selected = [rating for _, rating in user_movie_ratings]
    
    recommended_movies = get_similar_movies(movies_selected, ratings_selected, corr_matrix)

    # Flatten the list of recommended movies
    recommended_movies_flat = [movie for sublist in recommended_movies for movie in sublist]

    # Remove selected movies from the recommended movies list
    recommended_movies_unique = list(set(recommended_movies_flat) - set(selected_movies))

    # Take top 10 recommended movies
    recommended_movies_top10 = recommended_movies_unique[:10]

    recommended_movies_df = pd.DataFrame(recommended_movies_top10, columns=['Recommended_Movies'])

    # Merge recommended movies with the movies DataFrame
    movie_rec = pd.merge(recommended_movies_df, movies, left_on='Recommended_Movies', right_on='title')

    # Display recommended movies
    st.subheader("Recommended Movies:")

    # Define the number of columns for displaying recommended movies
    num_columns = 4

    # Calculate the number of rows needed to display all recommended movies
    num_movies = len(movie_rec)
    num_rows = (num_movies + num_columns - 1) // num_columns

    # Iterate over rows and columns to display recommended movies
    for i in range(num_rows):
        # Create columns for each row
        cols = st.columns(num_columns)
        for j in range(num_columns):
            # Calculate the index of the movie in the DataFrame
            index = i * num_columns + j
            # Check if the index is within the range of recommended movies
            if index < num_movies:
                # Display movie details in each column
                with cols[j]:
                    # Display movie title
                    st.write(movie_rec['title'].iloc[index])
                    # Display movie poster
                    st.image(fetch_poster(movie_rec['tmdbId'].iloc[index]), use_column_width=True)
                    # Display movie year
                    st.text(f"Year: {movie_rec['year'].iloc[index]}")
                    # Display movie genres
                    st.text(f"Genres: {movie_rec['genres'].iloc[index]}")
