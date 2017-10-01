import os
from flask import Flask,g
import sqlite3
from flask_login import LoginManager
from user import User


app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db/survey.db'),
    USERNAME="admin",
    PASSWORD="default"
))


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    return User(userid)
