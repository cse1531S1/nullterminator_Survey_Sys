from flask import Flask, redirect, render_template, request, url_for
from server import app
from question import quest_tree,addQ,delQ,getQ

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

@app.route("/delquest",methods= ["POST","GET"])
def del_question():
    # instance of quest_tree
    qt = quest_tree()
    if request.method== "POST":
        # try to delete the question that uesr want
        # create the instance of del_question class
        # initial an instance of deleting question
        del_q = delQ(qt)

        del_q.doDel(request.form.getlist("qid"))
        return render_template("success_del_q.html", request = url_for("del_question"))
    # a instance for finding all the question
    get_q = getQ(qt)
    # a list for question
    q_list = get_q.findQ()
    return render_template("del_q.html",request= url_for("del_question"),q_list = q_list)
