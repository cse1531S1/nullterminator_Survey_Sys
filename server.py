from flask import Flask
app = Flask(__name__)

# config things
app.config["SECRET_KEY"] = "Highly secret key"
# this part is for login credential
app.config["USERNAME"] = "admin"
app.config["PASSWORD"] = "default"
