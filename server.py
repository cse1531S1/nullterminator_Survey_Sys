from flask import Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"
app.config.update(dict(
    USERNAME="admin",
    PASSWORD="default"
))
