from flask import Flask, redirect, render_template, request, url_for
from server import app
from question import quest_tree,addQ,delQ,getQ
from survey import *
import csv



@app.route("/")
def index():
    return "hello world! - This is our website"


##THis function is being used when teacher click no question for their survey, and it could return a warning web page.
@app.route("/coursepage/warning", methods=["GET", "POST"])
def warning():
    return("hey, please go back and add your answer!")




##THis function is used read in the generated coursequestion.csv file, and make it a courselist.
## after that, you could print out the coursequestionlist to show waht is your final survey
@app.route("/coursepage/<string:coursename>/finalsurvey", methods=["GET", "POST"])
def finalsurvey(coursename):
    s = survey()
    return render_template("finalsurvey.html", course_name=coursename, questionfield=s.coursequestionlist(coursename),length=len(s.coursequestionlist(coursename)), number_of_answer=s.list_number_of_answer(s.coursequestionlist(coursename)) )




##first, it will show all the question have been created.
##Then, teacher chooses his desired questions
##All the questions being chosen will be used to create a csv file
## if no question chosen, it won't create csv file.
@app.route("/addquestions/<string:coursename>", methods=["GET", "POST"])
def addquestions(coursename):
    s = survey()
    # var for passing error message
    error = None
    # generated the list of questions
    get_question = getQ(quest_tree())
    if request.method == "POST":
        selected_q = request.form.getlist("selected_q")
        if selected_q != []:
            # the admin has selected some questions for this survey

            s.choosequestion(get_question.findQ(selected_q),coursename) #create a csv file
            return redirect(url_for('finalsurvey',coursename=coursename))
        else:
            # print ("here ")
            error = "please add at least one question for this survey."

    # getting all the question
    q_list = get_question.findQ()
    return render_template("surveycreate.html", course_name=coursename, quest_list=q_list, error = error)


##THis is the function to show all the course
##The return statement of function course() is the list of all the function
@app.route("/selectcourse", methods=["GET", "POST"])
def course_adding():
    s = survey()
    if request.method == "POST":
        return redirect(url_for('addquestions', coursename=request.form["co"]))
    return render_template("courselect.html", course_list=s.courselist() )


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
