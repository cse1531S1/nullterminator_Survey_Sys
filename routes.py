from flask import Flask, redirect, render_template, request, url_for,session
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from server import app,load_user
from survey import *
from respond import Respond
# from respond import respondent
from user import User,UserData,EnrolRequest
# import the new question
from question import Question
from enrolment import enrol_Data

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
#This isnt going to the login page first...
def login():
    # to record the error message
    error = None
    if request.method == "POST":
        try:
            this_user = load_user(request.form.get("username",None))
            if this_user.check_pass(request.form["password"]):
                # valid usesr

                login_user(User(request.form.get("username",None)))
                return redirect(url_for("dashboard"))
        except Exception as e:
            # write the error pront
            error = format(e)


    return render_template("login.html",msg_err = error)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"), code=302, Response=None)

@app.route("/register",methods=["POST","GET"])
def register():
    error =None
    if request.method == "POST":
        if request.form['pw']== request.form['re_pw']:
            try:
                UserData().register(request.form['id'], request.form['pw'])
                return render_template("msg.html",msg_suc_l=[
                    'Successful Register',"Wait for admin to approve your request.",
                    url_for('index'),"Return to Home Page"
                ])
            except Exception as e:
                # extract the mesage of error
                error = format(e)
        else:
            error = "Password provided is not same."

    # Render pront for register
    return render_template("register.html",msg_err = error)



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
                course_l= c.get_course(),guest_l = UserData().show_unguest(),\
                enrol_l = EnrolRequest().get_requests())
    if current_user.is_guest():
        return render_template('dash/guest.html',\
                    survey_l = s.get_survey_by_user(current_user.uid),\
                    course_l= c.get_course())



# survey creation in this controller
@app.route("/create_sur")
@app.route("/create_sur/<string:course_name>/<string:course_year>",methods=["GET","POST"])
@login_required
def survey_create(course_name=None,course_year=None):

    if not current_user.is_admin():
        # permission deny
        return redirect(url_for("permission_deny"))


    # variable to store the error message
    error = None

    # initial the instance to reach database
    s = Survey()
    c = Course()
    q = Question()

    # check whether this course has been already created a survey
    this_course = s.get_survey(course_name, course_year)

    # the user try to create a survey
    if request.method == "POST":


        # get all the selected question
        q_id = request.form.getlist("qid")

        if not  (request.form.get("s0") and request.form.get("s1")\
            and request.form.get("e0") and request.form.get("e1")):
            # no specify survey time error
            error = "Please specify time for this survey"
        if not error:
            # not error
            start_time =request.form.get("s0")+" "+request.form.get("s1")
            end_time = request.form.get("e0")+" "+request.form.get("e1")
            try:

                # the admin has selected some questions for this survey
                this_id = s.create_survey(course_name,course_year,q_id,start_time,end_time)
                # if not error
                # renturn a preview of final survey
                return redirect(url_for('view_survey', survey_id = this_id))
            except Exception as e:
                # grep the error pront
                error = format(e)



    if not course_name and not course_year:
        # name is none when teacher try to create a course
        return render_template("select_course.html",\
                    course_l = c.get_course())
    if this_course:
        # couldn't Create mutiple survey
        # return the error message for already have a survey for this_courses
        return render_template("msg.html",title= "Too Much Survey",\
                    msg_suc_l=["Survey Creation Error: Too Much Survey",\
                    "Too much survey for course "+course_name+" "+ course_year+".",\
                    url_for("dashboard"),"Back to Dashboard."])
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
def view_survey(survey_id=None):
    if current_user.is_student():
        return redirect(url_for("permission_deny"))

    q = Question()
    s = Survey()
    error = None

    if request.method == "POST":
        # request for changing
        selected_Qid = s.get_qids(survey_id)
        # record the mandertory question
        q_force = []

        if selected_Qid and current_user.is_staff():
            # in the staff, they only can choose not mendatory_q
            # filter out all the mandertory question
            q_force = q.find_q(q_id=selected_Qid, pool_id = "0")
            # change the q_force to  normal type(ids) == str
            q_force = [str(this_q[0]) for this_q in q_force]
        # get all the selected question
        q_id = request.form.getlist("qid")
        # save the changes, by reconstruct the question list
        # merge two ids into one array
        q_id+= q_force
        s.update_survey(survey_id, q_id)
        if not q_id:
            error = ["Survey Create Error: Not Sufficient Question",\
                    "Please select at least one question.",\
                    url_for("view_survey",survey_id= survey_id),\
                    "Continue Review This Survey"]

        if not error and request.form["submit_type"] == "save":
            # show the saved survey
            pass

        elif not error and request.form["submit_type"] == "post":
            #  post to next stage
            return redirect(url_for("post_survey",survey_id = survey_id))
    # find the specify survey by id
    this_survey = s.find("survey.id", survey_id).one()
    # find the selected question
    # change the type to match the filter
    selected_Qid = s.get_qids(survey_id)
    # get the survey status by indent
    survey_status = int(this_survey[6])


    if selected_Qid:
        # filter the selected question
        q_force = q.find_q(q_id = selected_Qid,pool_id = "0")
        q_opt = q.find_q(q_id = selected_Qid,pool_id = "1")
    else:
        # overwrite the qfind muti reaction
        q_force = []
        q_opt = []


    if current_user.is_admin():
        # have the right to edit all the added question
        return render_template("final_survey.html", course_name=this_survey[1],\
                    course_year = this_survey[2],\
                    mendatory_q = q.find_q(pool_id = "0"),list_type = ["check","check"],\
                    optional_q = q.find_q(pool_id = "1"),select_q = selected_Qid,\
                    survey_id = survey_id,msg_err_l = error,survey_status= survey_status)
    elif current_user.is_staff():
        # only have the right to review the question
        # find the course that has recorded in the survey
        return render_template("final_survey.html", course_name=this_survey[1],\
                    course_year = this_survey[2],\
                    mendatory_q = q_force,list_type = ["num","check"],\
                    optional_q = q.find_q(pool_id= "1"),select_q = selected_Qid,\
                    survey_id = survey_id,msg_err_l = error,survey_status= survey_status)


# delect survey in this controller
@app.route("/delete_sur")
@app.route("/delete_sur/<int:survey_id>",methods=["GET","POST"])
@login_required
def delete_survey(survey_id=None):
    # error handling
    if not current_user.is_admin:
        return redirect(url_for("permission_deny"))
    s = Survey()
    s.delete_survey(survey_id)
    return redirect(url_for('dashboard'))


# post survey in this controller
@app.route("/post_survey/<int:survey_id>")
@login_required
def post_survey(survey_id ):
    if current_user.is_student():
        return redirect(url_for("permission_deny"))

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
            return redirect(url_for("permission_deny"))
    # give a pront to show the successful message
    return render_template("msg.html",title= "Successfully Post a Survey",\
                msg_suc_l=["Successful Post a Survey",\
                "You were successfully posted survey "+str(survey_id)+".",\
                url_for("dashboard"),"Review More"])


@app.route("/close/<int:survey_id>")
@login_required
def close_survey(survey_id):
    # this controller only for admin to close a survey
    if not current_user.is_admin():
        # permission restriction
        return redirect(url_for("permission_deny"))

    s = Survey().close(survey_id)
    # give a pront to show the successful message
    return render_template("msg.html",title= "Successful Close a Survey",\
                msg_suc_l=["Successful Close a Survey",\
                "You were successfully Close survey "+str(survey_id)+".",\
                url_for("dashboard"),"Back to Dashboard"])


@app.route("/student/<int:survey_id>", methods=["GET", "POST"])
@login_required
def student(survey_id):
    # neccessary instance for survey creation
    s = Survey()
    res = Respond()
    error = None
    if current_user.is_admin() or current_user.is_staff():
        # the Admin and staff can preview the survey
        pass
    elif res.is_submitted(survey_id, current_user.get_id()) or \
    not (current_user.is_student() or current_user.is_guest()):
        return redirect(url_for("permission_deny"))

    # get the basic information for this survey_id
    this_survey = s.id_filter(survey_id).one()
    qids = s.get_qids(survey_id)
    if request.method == "POST":
        answerlist = []
        for qid in qids:
            try:
                # get all the answer form student
                # because the questoin_id in survey is start form 1
                # so add 1 in i and find the answer
                this_q = request.form[str(qid)]
                if not this_q:
                    error = "You must finish all the questions."
                answerlist.append(this_q)
            except :
                error = "You must finish all the questions."
        if not error:
            # push the recorded answers to database
            res.new_res(survey_id, current_user.get_id(), answerlist)
            return render_template("finish_survey.html")
    # get the question information form here
    q = Question()
    # all the question is here
    q_list = q.find_q(qids)


    return render_template("student.html", \
            course_name = this_survey[1]+" "+this_survey[2],\
            msg_err = error,\
            quest_list = q_list)


@app.route("/quest",methods = ["POST","GET"])
@login_required
def add_question():
    if not current_user.is_admin():
        # permission deny
        return redirect(url_for("permission_deny"))
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
        return redirect(url_for("permission_deny"))
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
@app.route("/results/<int:survey_id>",methods=["GET","POST"])
@login_required
def show_results(survey_id = None):
    if not survey_id:
        # not seeing the results
        return redirect("dash")
    # name is no none, try to find the results of that survey
    # instance for getting results
    res = Respond()

    return render_template("results.html",results=res.get_results(survey_id))

@app.route('/enrol/<int:course_id>')
@login_required
def enrol(course_id):
    # enrol for guest
    if not current_user.is_guest():
        return redirect(url_for('permission_deny'))
    # record the error message
    error = None
    # sent this request to system
    try:
        current_user.enrol(course_id)
        # successful add this message
    except Exception as e:
        # not place to pront the error...
        error = format(e)
    if error:
        return render_template("msg.html",msg_err_l = [
            'Error:',error,url_for("dashboard"),'Return to Dashboard'])
    else:
        return render_template("msg.html",msg_suc_l=[
            "Successful Request","Your enrol has been sent to admin.",\
            url_for('dashboard'),"Return to Dashboard"
            ])

@app.route("/reqest_approve/<int:require_id>")
def request_approve(require_id):
    # admin approve enrol request
    if not current_user.is_admin:
        return redirect(url_for('permission_deny'))
    try:
        # use the admin privilage to approve a request
        current_user.premit_enrol(require_id)
        return render_template("msg.html",msg_suc_l=[
            "Approve Request","Approve request for enrolment "+str(require_id),
            url_for('dashboard'),'Back to Dashboard'
            ])
    except Exception as e:
        error = format(e)
    return render_template("msg.html",msg_err_l=[
             "Error",error,
             url_for('dashboard'),'Back to Dashboard'
             ])



@app.route('/request_deny/<int:require_id>')
def request_deny(require_id):
    # admin approve enrol request
    if not current_user.is_admin:
        return redirect(url_for('permission_deny'))
    try:

        # use the admin privilage to deny a enrol requested
        current_user.deny_enrol(require_id)

        return render_template("msg.html",msg_suc_l=[
            "Denied Request","Deny the request for enrolment "+str(require_id),
            url_for('dashboard'),'Back to Dashboard'
            ])
    except Exception as e:
        error = format(e)
    # print the error message
    return render_template("msg.html",msg_err_l=[
             "Error",error,
             url_for('dashboard'),'Back to Dashboard'
             ])



@app.route('/premit_register/<int:user_id>')
def premit_register(user_id):
    # admin approve enrol request
    if not current_user.is_admin:
        return redirect(url_for('permission_deny'))
    # admin to delete a user
    current_user.permit_register(user_id)
    # return the successful pront
    return render_template("msg.html",msg_suc_l=['Successful Authentication',
        "You have successfully authenticate user "+str(user_id)+" as a guest user.",
        url_for('dashboard'),"Back to Dashboard"
        ])

@app.route('/deny_register/<int:user_id>')
def deny_register(user_id):
    # admin approve enrol request
    if not current_user.is_admin:
        return redirect(url_for('permission_deny'))
    # delete that user in database by admin
    current_user.deny_register(user_id)
    # return the successful pront
    return render_template("msg.html",msg_err_l=['Successful Delete',
        "You have successfully delete user "+str(user_id)+" in database.",
        url_for('dashboard'),"Back to Dashboard"
        ])


# page for not permission
@app.route("/permission")
def permission_deny():
    return render_template("permission.html")
