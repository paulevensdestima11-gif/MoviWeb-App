from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import db

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
    try:
        movies = data_manager.get_movies(user_id)
        return render_template('movies.html', movies=movies, user_id=user_id)

    except Exception as e:
        print("Error loading movies:", str(e))
        return render_template('404.html'), 404


# -------------------
# ADD MOVIE
# -------------------
@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    try:
        movie = {
            "name": request.form.get("name"),
            "director": request.form.get("director"),
            "year": request.form.get("year"),
            "poster_url": request.form.get("poster_url"),
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
    return render_template('404.html'), 404


# -------------------
# RUN APP
# -------------------
if __name__ == "__main__":
    app.run(debug=True)