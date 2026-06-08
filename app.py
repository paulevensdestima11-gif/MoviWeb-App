from flask import Flask
from data_manager import DataManager
from models import db, Movie

app = Flask(__name__)

# -------------------
# DATABASE CONFIG
# -------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

data_manager = DataManager()


# -------------------
# HOME ROUTE (TEST)
# -------------------
@app.route('/')
def home():
    return "Welcome to MoviWeb App!"


# -------------------
# USERS ROUTE (DATA MANAGER INTEGRATION)
# -------------------
@app.route('/users')
def list_users():
    users = data_manager.get_users()
    return str(users)


# -------------------
# CREATE DATABASE
# -------------------
with app.app_context():
    db.create_all()


# -------------------
# RUN APP
# -------------------
if __name__ == "__main__":
    app.run(debug=True)