"""
MoviWeb Flask Application

This application allows users to manage their favorite movies.
Users can be created, and movies can be added, updated, viewed,
and deleted from a user's movie collection.

"""

from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import db
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OMDB_API_KEY")

app = Flask(__name__)

# -------------------
# DATABASE CONFIG
# -------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

data_manager = DataManager()

# -------------------
# CREATE DATABASE
# -------------------
with app.app_context():
    db.create_all()


# -------------------
# HOME PAGE (LIST USERS)
# -------------------
@app.route('/')
def index():
    """
    Display all registered users.

    Returns:
        Rendered index page containing the list of users.
    """
    try:
        users = data_manager.get_users()
        return render_template('index.html', users=users)
    except Exception as e:
        print("Error loading users:", str(e))
        return render_template('404.html'), 500


# -------------------
# CREATE USER
# -------------------
@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user and store it in the database.

    Returns:
        Redirect to the home page.
    """
    try:
        name = request.form.get("name")

        if not name:
            return redirect(url_for('index'))

        data_manager.create_user(name)
        return redirect(url_for('index'))

    except Exception as e:
        print("Error creating user:", str(e))
        return render_template('404.html'), 500


# -------------------
# SHOW USER MOVIES
# -------------------
@app.route('/users/<int:user_id>')
def get_movies(user_id):
    """
    Display all movies belonging to a specific user.

    Args:
        user_id (int): ID of the selected user.

    Returns:
        Rendered movies page.
    """
    try:
        movies = data_manager.get_movies(user_id)
        user = data_manager.get_user(user_id)

        return render_template(
            'movies.html',
            movies=movies,
            user=user,
            user_id=user_id
        )

    except Exception as e:
        print("Error loading movies:", str(e))
        return render_template('404.html'), 404

# -------------------
# ADD MOVIE
# -------------------
@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """
    Add a movie using OMDb API.
    """
    try:
        title = request.form.get("title")

        if not title:
            return redirect(url_for('get_movies', user_id=user_id))

        url = (
            f"https://www.omdbapi.com/"
            f"?t={title}&apikey={API_KEY}"
        )

        response = requests.get(url)
        data = response.json()

        if data.get("Response") == "False":
            print("Movie not found.")
            return redirect(url_for('get_movies', user_id=user_id))

        movie = {
            "name": data.get("Title"),
            "director": data.get("Director"),
            "year": int(data.get("Year", "0").split("–")[0]),
            "poster_url": data.get("Poster"),
            "user_id": user_id
        }

        data_manager.add_movie(movie)

        return redirect(url_for('get_movies', user_id=user_id))

    except Exception as e:
        print("Error adding movie:", str(e))
        return redirect(url_for('get_movies', user_id=user_id))

# -------------------
# UPDATE MOVIE TITLE
# -------------------
@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """
    Update the title of an existing movie.

    Args:
        user_id (int): ID of the user.
        movie_id (int): ID of the movie to update.

    Returns:
        Redirect to the user's movie page.
    """
    try:
        new_title = request.form.get("title")
        data_manager.update_movie(movie_id, new_title)

        return redirect(url_for('get_movies', user_id=user_id))

    except Exception as e:
        print("Error updating movie:", str(e))
        return redirect(url_for('get_movies', user_id=user_id))


# -------------------
# DELETE MOVIE
# -------------------
@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
    Delete a movie from a user's collection.

    Args:
        user_id (int): ID of the user.
        movie_id (int): ID of the movie to delete.

    Returns:
        Redirect to the user's movie page.
    """
    try:
        data_manager.delete_movie(movie_id)
        return redirect(url_for('get_movies', user_id=user_id))

    except Exception as e:
        print("Error deleting movie:", str(e))
        return redirect(url_for('get_movies', user_id=user_id))


# -------------------
# 404 ERROR HANDLER
# -------------------
@app.errorhandler(404)
def page_not_found(e):
    """
    Handle requests for non-existing pages.

    Args:
        e: Flask exception object.

    Returns:
        Custom 404 error page.
    """
    return render_template('404.html'), 404


# -------------------
# RUN APP
# -------------------
if __name__ == "__main__":
    app.run(debug=True)