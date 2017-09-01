from flask import Flask, redirect, render_template, request, url_for
from server import app
from question import quest_tree,addQ

@app.route("/")
def index():
    return "hello world! - This is our website"


@app.route("/quest",methods = ["POST","GET"])
def add_question():
    if request.method == "POST":
        # get the question set
        add_q = addQ(quest_tree())
        # grap the user input
        question = request.form["question"]
        answers = request.form["answers"].split(",")
        if add_q.is_valid_Q(question,answers) == 0:
            # valid input
            # push the user input into system
            add_q.add_Q(question, answers)
            # get back the successful page to user
            return render_template("success_add_q.html",add_more = url_for("add_question"))
        # invalid input, push back what user has been input, and push the error message
        return render_template("add_q.html",request = url_for("add_question"),error = add_q.is_valid_Q(question,answers),question = question, answers = request.form["answers"])
    return render_template("add_q.html",request = url_for("add_question"))
