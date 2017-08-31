from flask import Flask, redirect, render_template, request, url_for,session,flash
from server import app


@app.route("/")
def index():
    return "hello world! - This is our website"


@app.route("/login",methods= ['GET','POST'])
def login():
    error = None
    if request.method== "POST":
        # trying to login
        if request.form['username']== app.config["USERNAME"] and\
            request.form['password']== app.config["PASSWORD"]:
            # valid credential
            session['logged_in'] = True
            return redirect(url_for("manage"))
        else:
            error = "Invalid password or username"
    return render_template("login.html",error= error,login_page = url_for("login"))

@app.route('/logout')
def logout():
    session.pop("logged_in",None)
    flash("You were logged out")
    return redirect(url_for("index"))

@app.route("/manage")
def manage():
    if session['logged_in']:
        # valid user
        return render_template("manage.html")

    # invalid user, send it back to login
    return redirect(url_for("login"))
