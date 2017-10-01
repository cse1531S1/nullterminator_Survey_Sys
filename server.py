import os
from flask import Flask,g
import sqlite3
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"
login_manager = LoginManager()
login_manager.init_app(app)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db/survey.db'),
))

def get_db():

    if not hasattr(g,'sqlite_db'):
        # initial a connection
        g.sqlite_db =sqlite3.connect(app.config['DATABASE'])
    return g.sqlite_db


# # disconnect the database
@app.teardown_appcontext
def teardown_db(exception):
    # with app.app_context():
    if hasattr(g, 'sqlite_db'):
        # commit all the changes for this thread
        # (delay all the commit, so the website could act more reponsive)
        g.sqlite_db.commit()

        g.sqlite_db.close()
    else:
        print("the database has disconnected already")
