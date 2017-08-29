from flask import Flask, redirect, render_template, request, url_for
from server import app
from question import quest_tree,addQuestion

@app.route("/")
def index():
    return "hello world! - This is our website"


@app.route("/quest",methods = ["POST","GET"])
def addQuestion():
    if request.method == "POST":
        quests2 = quest_tree()
        # add_q = addQuestion(quests2)
        # question = request.form["question"]
        # answers = request.form["answers"].split(",")
        # if add_q.is_valid_Q(question,answers) == 0:
        #     return render_template("success_add_q.html")
        return render_template("add_q.html",request = url_for("addQuestion"),error = add_q.is_valid_Q(question,answers),question = question, answers = request.form["answers"])
    return render_template("add_q.html",request = url_for("addQuestion"))
