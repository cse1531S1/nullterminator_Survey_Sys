import os
from flask import Flask,g
import sqlite3
from flask_login import LoginManager
from user import UserData,Staff,Admin,Student,Guest


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
    usr = UserData()
    if not userid:
        raise TypeError("Please provide your user id.")
    try:
        role = usr.findById(int(userid))[2]
    except Exception as e:
        raise TypeError("Wrong username/password, please try again.") 
    # initialise the class by the role
    if role == 'admin':
        return Admin(userid)
    elif role == 'student':
        return Student(userid)
    elif role in ["guest","unguest"] :
        return Guest(userid)
    elif role == 'staff':
        return Staff(userid)
