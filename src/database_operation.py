import sqlite3
import subprocess

def insert_movie(conn, movieId, title, year, genres, tmdbId):
    # Insert a new movie into the 'movies' table.
    cursor = conn.cursor()
    cursor.execute("INSERT INTO movies (movieId, title, year, genres, tmdbId) VALUES (?, ?, ?, ?, ?)",
                   (movieId, title, year, genres, tmdbId))
    conn.commit()
    print("Movie inserted successfully.")
    # After inserting, update the correlation matrix
    update_corr_matrix(conn)

def update_movie(conn, movieId, title, year, genres, tmdbId):
    # Update an existing movie in the 'movies' table.
    cursor = conn.cursor()
    cursor.execute("UPDATE movies SET title=?, year=?, genres=?, tmdbId=? WHERE movieId=?",
                   (title, year, genres, tmdbId, movieId))
    conn.commit()
    print("Movie updated successfully.")
    # After updating, update the correlation matrix
    update_corr_matrix(conn)

def delete_movie_by_title(conn, title):
    # Delete a movie from the 'movies' table based on its title.
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE title=?", (title,))
    conn.commit()
    print("Movie deleted successfully.")
    # After deleting, update the correlation matrix
    update_corr_matrix(conn)

def delete_movie_by_id(conn, movieId):
    # Delete a movie from the 'movies' table based on its movieId.
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE movieId=?", (movieId,))
    conn.commit()
    print("Movie deleted successfully.")
    # After deleting, update the correlation matrix
    update_corr_matrix(conn)

def connect_to_database(database_path):
    # Connect to the SQLite database.
    conn = sqlite3.connect(database_path)
    return conn

def close_connection(conn):
    # Close connection to the SQLite database.
    conn.close()

def update_corr_matrix(conn):
    # Run matrix.py to update the correlation matrix
    subprocess.run(["python", "matrix.py"])

if __name__ == "__main__":
    # Connect to the SQLite database
    database_path = r'../MOVIE-RECOMMENDER-SYSTEM/database/data.db'
    conn = connect_to_database(database_path)

    # Ask user for action
    action = input("Enter action (insert/update/delete): ")

    if action == "insert":
        # Insert a new movie
        movieId = input("Enter movieId: ")
        title = input("Enter title: ")
        year = input("Enter year: ")
        genres = input("Enter genres: ")
        tmdbId = input("Enter tmdbId: ")
        insert_movie(conn, movieId, title, year, genres, tmdbId)

    elif action == "update":
        # Update an existing movie
        movieId = input("Enter movieId to update: ")
        title = input("Enter new title: ")
        year = input("Enter new year: ")
        genres = input("Enter new genres: ")
        tmdbId = input("Enter new tmdbId: ")
        update_movie(conn, movieId, title, year, genres, tmdbId)

    elif action == "delete":
        # Ask user if they want to delete by title or movieId
        delete_option = input("Enter delete option (title/movieId): ")

        if delete_option == "title":
            # Delete a movie by title
            title = input("Enter title to delete: ")
            delete_movie_by_title(conn, title)
        elif delete_option == "movieId":
            # Delete a movie by movieId
            movieId = input("Enter movieId to delete: ")
            delete_movie_by_id(conn, movieId)
        else:
            print("Invalid delete option. Please enter 'title' or 'movieId'.")

    else:
        print("Invalid action. Please enter 'insert', 'update', or 'delete'.")

    # Close connection
    close_connection(conn)