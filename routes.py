from flask import Flask, redirect, render_template, request, url_for,session
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from server import app
from survey import *
# from respond import respondent
from user import User
# import the new question
from question import Question
from enrolment import enrol_Data

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
@app.route("/dashboard")
@login_required
def dashboard():
    # route by the current user type
    c= Course()
    # get the survey instance
    s = Survey()


    # muti type of user respond
    if current_user.is_student():
        return render_template('dash/student.html',\
                survey_l = s.get_survey_by_user(current_user.uid))
    if current_user.is_staff():
        return render_template('dash/staff.html',\
                survey_l = s.get_survey_by_user(current_user.uid))
    if current_user.is_admin():
        # get all the ongoning survey and all the courses
        return render_template('dash/admin.html',survey_l = s.get_survey(),\
                course_l= c.get_course())




# survey creation in this controller
@app.route("/create_sur")
@app.route("/create_sur/<string:course_name>/<string:course_year>",methods=["GET","POST"])
@login_required
def course_adding(course_name=None,course_year=None):

    s = Survey()
    c = Course()
    if not current_user.is_admin():
        redirect(url_for("index"),msg_err = "You have not premission to create a survey")

    if not course_name and not course_year:
        # name is none when teacher try to create a course
        return render_template("courselect.html",\
                    course_l = c.get_course())
    # else: admin already have select a course
    # admin go to a specific survey of {course_name}{course_year}
    this_survey = s.get_survey(course_name,course_year)
    return render_template("select_sur.html", course_name = course_name,course_year = course_year,survey = this_survey)



# delect survey in this controller
@app.route("/delete_sur")
@app.route("/delete_sur/<int:survey_id>",methods=["GET","POST"])
@login_required
def delete_survey(survey_id=None):
    # error handling

    s = Survey()
    s.delete_survey(survey_id)
    return redirect(url_for('dashboard'))


# post survey in this controller
@app.route("/sur_to_staff/<string:course_name>/<string:course_year>",methods=["GET"])
@login_required
def post_sur_to_staff(course_name=None,course_year=None):

      s = Survey()
      this_survey = s.post_sur_to_staff(course_name,course_year)
      return render_template("select_sur.html", course_name = course_name,course_year = course_year,survey = this_survey)




# create survey in the controller
@app.route("/view_sur/<string:course_name>/<string:course_year>",methods=["GET","POST"])
@login_required
def survey_create(course_name=None,course_year=None):

    s = Survey()
    q = Question()
    get_genQ = q.find_q(pool_id = "0")
    get_optQ = q.find_q(pool_id = "1")
    error = None

    if request.method == "POST":
        selected_genQ = request.form.getlist("selected_genQ")
        selected_optQ = request.form.getlist("selected_optQ")
        q_id = selected_genQ + selected_optQ
        start_time = request.form.get("s0")+" "+request.form.get("s1")
        end_time = request.form.get("e0")+" "+request.form.get("e1")
        if selected_genQ != []:
            # the admin has selected some questions for this survey
            this_id = s.create_survey(course_name,course_year,q_id,start_time,end_time)
            # renturn a preview of final survey
            return redirect(url_for('view_survey', survey_id = this_id,course_name = course_name, course_year = course_year))

        else:
            error = "Please add at least one general question for this survey."

    return render_template("surveycreate.html", course_name=course_name,\
    course_year=course_year,genQ_list=get_genQ,\
    optQ_list=get_optQ,msg_err = error)






# view survey in this controller
@app.route("/view_sur/<int:survey_id>/<string:course_name>/<string:course_year>",methods=["GET","POST"])
@login_required
def view_survey(survey_id=None,course_name=None,course_year=None):
   print("test")
   q = Question()
   s = Survey()
   this_survey = s.get_survey(course_name,course_year)
   selected_Qid = this_survey[3].split("&&")
   q_force = q.find_q(q_id = selected_Qid,pool_id = "0")
   q_opt = q.find_q(q_id = selected_Qid,pool_id = "1")
   return render_template("finalsurvey.html", course_name=course_name,\
                course_year = course_year,\
                genlist = q_force,\
                 optlist = q_opt,\
                 Qnum1=len(q_force),\
                 Qnum2=len(q_opt))






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
    if current_user.is_student():
        return redirect(url_for("index"),\
                msg_err = "You have not primission for"+url_for("del_question"))

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
    if not current_user.is_admin():
        return redirect(url_for("index"),\
                msg_err = "You have not primission for"+url_for("del_question"))
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
