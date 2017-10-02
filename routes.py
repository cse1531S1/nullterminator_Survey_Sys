from flask import Flask, redirect, render_template, request, url_for,session
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from server import app
from new_survey import *
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
    
            login_user(User(request.form.get("username",None)))
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
    c= Course()
    #print(current_user.user.is_admin)
    if current_user.is_student():
        return render_template('dash/student.html',survey_l = c.get_course())
    if current_user.is_staff():
        return render_template('dash/staff.html',survey_l = c.get_course())
    if current_user.is_admin():
        return render_template('dash/admin.html',survey_l = c.get_course())




# survey creation in this controller
@app.route("/create_sur")
@app.route("/create_sur/<string:course_name>/<string:course_year>",methods=["GET","POST"])
@login_required
def course_adding(course_name=None,course_year=None):

    s = Survey()
    c = Course()
    if not course_name and not course_year:
        # name is none when teacher try to create a course
        # render the course selection page
        # return render_template("courselect.html",\
                # course_list=c.get_course())
     
        return render_template("courselect.html",\
                    course_list = c.get_course())
    # else: teacher already have select a course
    # var for passing error message
    error = None
    # generated the list of questions
    ###get_question = getQ(quest_tree())
    q = Question()
    get_genQ = q.find_q(pool_id = "0")
    get_optQ = q.find_q(pool_id = "1") 
    if request.method == "POST":


        # teacher is trying to create a survey by select questions
        # getting all the teacher selected question
        selected_genQ = request.form.getlist("selected_genQ")
        selected_optQ = request.form.getlist("selected_optQ")
        if selected_genQ != [] and selected_optQ != []:
            # the admin has selected some questions for this survey
            this_id = s.create_survey(course_name,course_year,selected_genQ,selected_optQ,"2017-09-23 00:00:00","2017-09-23 23:59:59")          
            # renturn a preview of final survey
            view_survey(this_id,course_name,course_year)


    # teacher have select a course but not have select a question yet
    # getting all the question

    if s.get_survey(course_name,course_year) == []:
      return render_template("surveycreate.html", course_name=course_name,\
         course_year=course_year,genQ_list=get_genQ,\
         optQ_list=get_optQ, msg_err = error)

    else :
      return render_template("select_sur.html", course_name = course_name, course_year = course_year,survey_l = s.get_survey(course_name,course_year))


@app.route("/view_survey")
@app.route("/view_sur/<string:course_name>/<string:course_year>",methods=["GET","POST"])
@login_required
def view_survey(survey_id= 1,course_name="",course_year=""):
   
   q = Question()
   get_genQ = q.find_q(pool_id = "0")
   get_optQ = q.find_q(pool_id = "1")
   s = Survey()
   survey_list = s.get_survey(course_name,course_year)
   this_survey = s.get_survey_by_id(survey_id,survey_list)
   selected_genQ = this_survey[2].split("&&")
   selected_optQ = this_survey[3].split("&&")
   # renturn a preview of final survey
   return render_template("finalsurvey.html", course_name=course_name,\
                course_year = course_year,\
                genlist = q.find_q(q_id = selected_genQ,pool_id = "0"),\
                optlist = q.find_q(q_id = selected_optQ,pool_id = "1"),\
                Qnum1 = len(q.find_q(q_id = selected_genQ,pool_id = "0")),\
                Qnum2 = len(q.find_q(q_id = selected_genQ,pool_id = "1"))) 
        





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
