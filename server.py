from flask import Flask
app = Flask(__name__)

# config things
app.config["SECRET_KEY"] = "Highly secret key"
