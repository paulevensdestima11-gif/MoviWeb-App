"""
Data Manager for the MoviWeb application.

This module contains the DataManager class, which is responsible
for all database interactions. It provides CRUD operations for
users and movies.

Author: Paul Evens Destima
"""

from models import db, User, Movie


class DataManager:
    """
    Handles all database operations for users and movies.
    """

    def create_user(self, name):
        """
        Create and save a new user.

        Args:
            name (str): Name of the user.

        Returns:
            User: The newly created user object.
        """
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_users(self):
        """
        Retrieve all users from the database.

        Returns:
            list[User]: List of all users.
        """
        return User.query.all()

    def get_user(self, user_id):
        """
        Retrieve a single user by ID.

        Args:
            user_id (int): ID of the user.

        Returns:
            User | None:
                User object if found,
                otherwise None.
        """
        return User.query.get(user_id)

    def get_movies(self, user_id):
        """
        Retrieve all movies belonging to a specific user.

        Args:
            user_id (int): ID of the user.

        Returns:
            list[Movie]: List of movies belonging to the user.
        """
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        """
        Add a new movie to the database.

        Args:
            movie (dict): Dictionary containing movie information.

        Returns:
            Movie: The newly created movie object.
        """
        new_movie = Movie(
            name=movie["name"],
            director=movie["director"],
            year=movie["year"],
            poster_url=movie["poster_url"],
            user_id=movie["user_id"]
        )

        db.session.add(new_movie)
        db.session.commit()
        return new_movie

    def update_movie(self, movie_id, new_title):
        """
        Update the title of an existing movie.

        Args:
            movie_id (int): ID of the movie to update.
            new_title (str): New title for the movie.

        Returns:
            Movie | None:
                Updated movie object if found,
                otherwise None.
        """
        movie = Movie.query.get(movie_id)

        if movie:
            movie.name = new_title
            db.session.commit()
            return movie

        return None

    def delete_movie(self, movie_id):
        """
        Delete a movie from the database.

        Args:
            movie_id (int): ID of the movie to delete.

        Returns:
            bool:
                True if the movie was deleted,
                False if the movie was not found.
        """
        movie = Movie.query.get(movie_id)

        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True

        return False