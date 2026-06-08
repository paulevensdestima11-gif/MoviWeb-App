from flask import Flask
from data_manager import DataManager
from models import db, Movie

app = Flask(__name__)

# -------------------
# DATABASE CONFIG (ORM)
# -------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

data_manager = DataManager()


# -------------------
# HOME ROUTE (TEST ONLY)
# -------------------
@app.route("/")
def home():
    return "Welcome to MoviWeb App!"


# -------------------
# CREATE DATABASE FIRST TIME
# -------------------
with app.app_context():
    db.create_all()


# -------------------
# RUN APP
# -------------------
if __name__ == "__main__":
    app.run(debug=True)