import os
from flask import Flask,g
import sqlite3
app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db/survey.db'),
    USERNAME="admin",
    PASSWORD="default"
))

def get_db():
    with app.app_context():
        if not hasattr(g,'sqlite_db'):
            # initial a connection
            g.sqlite_db =sqlite3.connect(app.config['DATABASE'])
        return g.sqlite_db


# # disconnect the database
# @app.teardown_appcontext
# def teardown_db(exception):
#     with app.app_context():
#         db =getattr(g, 'sqlite_db', default=None)
#         if db:
#             db.close()
