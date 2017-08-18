from flask import Flask, redirect, render_template, request, url_for
from server import app


@app.route("/")
def index():
    return "hello world!"
