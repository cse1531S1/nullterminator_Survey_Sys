from flask import Flask, redirect, render_template, request, url_for,session
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from server import app
from survey import *
from respond import respondent
from user import User
from question import quest_tree,addQ,delQ,getQ
# import the new question
from new_question import Question


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
#This isnt going to the login page first...
def login():
    if request.method == "POST":
        this_user = User(request.form.get("username",None))

        if this_user.check_pass(request.form["password"]):
            # valid usesr
            login_user(User(2))
            return redirect(url_for("dashboard"))


    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"), code=302, Response=None)


@app.route("/dash")
@login_required
def dashboard():
    # route by the current user type

    """
    !!!! These functions are not complete, plz complete it by the new survey parts!
    When u complete it, delete this comment.
    The _***.html in the dash is just give u a brief idea about how to do this.
    Modify them by your data.
      """
    if current_user.is_student():
        return render_template('dash/student.html',survey_l = survey().courselist())
    if current_user.is_staff():
        return render_template('dash/staff.html',survey_l = survey().courselist())
    if current_user.is_admin():
        return render_template('dash/admin.html',survey_l = survey().courselist())




# survey creation in this controller
@app.route("/create_sur")
@app.route("/create_sur/<string:name>",methods=["GET","POST"])
@login_required
def course_adding(name=None):

    s = survey()
    if not name:
        # name is none when teacher try to create a course
        # render the course selection page
        return render_template("courselect.html", course_list=s.courselist())
    # else: teacher already have select a course
    # var for passing error message
    error = None
    # generated the list of questions
    get_question = getQ(quest_tree())
    if request.method == "POST":
        # teacher is trying to create a survey by select questions
        # getting all the teacher selected question
        selected_q = request.form.getlist("selected_q")
        if selected_q != []:
            # the admin has selected some questions for this survey
            s.choosequestion(get_question.findQ(selected_q),name) #create a csv file
            # renturn a preview of final survey
            return render_template("finalsurvey.html", course_name=name,\
                quest_list=s.coursequestionlist(name) )
        else:
            error = "Please add at least one question for this survey."
    # teacher have select a course but not have select a question yet
    # getting all the question
    q_list = get_question.findQ()
    return render_template("surveycreate.html", course_name=name,\
        quest_list=q_list, msg_err = error)






# @app.route("/student")
@app.route("/student/<string:name>", methods=["GET", "POST"])
@login_required
def student(name):
    s = survey()
    res = respondent(name)
    error = None
    length = res.get_length()
    questionlist = res.get_question()

    if request.method == "POST":
        answerlist = []
        for i in range(length):
            try:
                # get all the answer form student
                # because the questoin_id in survey is start form 1
                # so add 1 in i and find the answer
                answerlist.append(request.form[str(i+1)])
            except :
                error = "You must finish all the questions."
        print(answerlist)
        if not error:
            res.append_csv(answerlist)
            return render_template("finish_survey.html")

    return render_template("student.html", course_name = name, msg_err = error,\
        quest_list = questionlist,length = length)


@app.route("/quest",methods = ["POST","GET"])
@login_required
def add_question():


    error = ""
    # else: the admin has logged_in
    if request.method == "POST":
        quest = Question()
        # get the question set

        # grap the user input
        question = request.form["question"]
        answers = request.form["answers"].split("/")
        pool_id = request.form["pool_id"]
        q_type = request.form["type"]

        try:
            quest.add_q(question, pool_id, q_type, answers = answers)
        except TypeError as e:
            error = format(e)
        else:
            return render_template("success_add_q.html")


        # invalid input, push back what user has been input, and push the error message
        return render_template("add_q.html",\
            msg_err = error,question = question, \
            answers = request.form["answers"])
    return render_template("add_q.html")

@app.route("/delquest",methods= ["POST","GET"])
@login_required
def del_question():

    # instance of quest_tree
    quest = Question()
    error = None
    if request.method== "POST":
        # try to delete the question that uesr want
        # create the instance of del_question class
        # initial an instance of deleting question
        try:

            quest.del_q(request.form.getlist("qid"))
        except Exception as e:
            error = format(e)
        else:
            return render_template("success_del_q.html")

    # a list for question
    mendatory = quest.find_q(pool_id="0")
    optional = quest.find_q(pool_id=1)
    return render_template("del_q.html",\
    mendatory = mendatory,optional=optional,msg_err = error)

#Route to the results page displaying results of a survey.
#not sure how the data csv's are setup or how it should know which csv to read
@app.route("/results")
@app.route("/results/<string:name>",methods=["GET","POST"])
@login_required
def show_results(name = None):

    response = respondent(name)
    if not name:
        # find all classes

        return render_template("select_result.html",course_list =response.get_open_course() )
    # name is no none, try to find the results of that survey
    # get all the survey question

    results=response.get_results()

    return render_template("results.html",results=response.get_results())
