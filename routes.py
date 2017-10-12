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
def survey_create(course_name=None,course_year=None):

    if not current_user.is_admin():
        # premission deny
        return redirect(url_for("premission_deny"))


    # variable to store the error message
    error = None

    # initial the instance to reach database
    s = Survey()
    c = Course()
    q = Question()

    # the user try to create a survey
    if request.method == "POST":
        # get all the selected question
        q_id = request.form.getlist("qid")

        if not q_id:
            # no specify question error
            error = "Please add at least one question for this survey."
        if not  (request.form.get("s0") and request.form.get("s1")\
            and request.form.get("e0") and request.form.get("e1")):
            # no specify survey time error
            error = "Please specify time for this survey"
        else:
            # not error
            start_time =request.form.get("s0")+" "+request.form.get("s1")
            end_time = request.form.get("e0")+" "+request.form.get("e1")
            # the admin has selected some questions for this survey
            this_id = s.create_survey(course_name,course_year,q_id,start_time,end_time)
            # renturn a preview of final survey
            return redirect(url_for('view_survey', survey_id = this_id))



    if not course_name and not course_year:
        # name is none when teacher try to create a course
        return render_template("select_course.html",\
                    course_l = c.get_course())
    # else: admin already have select a course
    # the admin try to create a survey

    # find the question with different pool
    get_genQ = q.find_q(pool_id = "0")
    get_optQ = q.find_q(pool_id = "1")

    return render_template("survey_create.html", course_name=course_name,\
    course_year=course_year,mendatory_q=get_genQ,\
    optional_q=get_optQ,msg_err = error)


# view survey in this controller
@app.route("/survey_view/<int:survey_id>",methods=["GET","POST"])
@login_required
def view_survey(survey_id=None,course_name=None,course_year=None):
    if current_user.is_student():
        return redirect(url_for("premission_deny"))


    q = Question()
    s = Survey()
    # find the specify survey by id
    this_survey = s.find("survey.id", survey_id).one()

    # find the selected question
    # change the type to match the filter
    selected_Qid = [int(qid) for qid in this_survey[3].split("&&")]

    # filter the selected question
    q_force = q.find_q(q_id = selected_Qid,pool_id = "0")
    q_opt = q.find_q(q_id = selected_Qid,pool_id = "1")

    if current_user.is_admin():
        # have the right to edit all the added question
        return render_template("final_survey.html", course_name=this_survey[1],\
                    course_year = this_survey[2],\
                    mendatory_q = q.find_q(pool_id = "0"),list_type = ["check","check"],\
                    optional_q = q.find_q(pool_id = "1"),select_q = selected_Qid,survey_id = survey_id)
    elif current_user.is_staff():
        # only have the right to review the question
        # find the course that has recorded in the survey
        return render_template("final_survey.html", course_name=this_survey[1],\
                    course_year = this_survey[2],\
                    mendatory_q = q_force,list_type = ["num","check"],\
                    optional_q = q.find_q(pool_id= "1"),select_q = selected_Qid,survey_id = survey_id)


# delect survey in this controller
@app.route("/delete_sur")
@app.route("/delete_sur/<int:survey_id>",methods=["GET","POST"])
@login_required
def delete_survey(survey_id=None):
    # error handling
    if not current_user.is_admin:
        return redirect(url_for("premission_deny"))
    s = Survey()
    s.delete_survey(survey_id)
    return redirect(url_for('dashboard'))


# post survey in this controller
@app.route("/post_survey/<int:survey_id>")
@login_required
def post_survey(survey_id ):
    if current_user.is_student():
        return redirect(url_for("premission_deny"))

    s = Survey()
    if current_user.is_admin():
        # admin want to post the survey to staff
        s.post(survey_id)
    elif current_user.is_staff():
        # staff try to post this survey to student
        if s.is_premitted(survey_id, current_user.get_id()):
            # the staff is in that course
            s.review(survey_id)
        else:
            # the staff have no right to change the code
            return redirect(url_for("premission_deny"))
    # give a pront to show the successful message
    return render_template("msg.html",title= "Successful Post a Survey",\
                msg_suc_l=["Successful Post a Survey",\
                "You were successfully posted survey "+str(survey_id)+".",\
                url_for("dashboard"),"Review More"])



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
        return redirect(url_for("premission_deny"))

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
        return redirect(url_for("premission_deny"))
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
    mendatory_q = mendatory,optional_q=optional,msg_err = error)

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

# page for not premission
@app.route("/premission")
def premission_deny():

    return render_template("premission.html")
