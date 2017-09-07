from flask import Flask, redirect, render_template, request, url_for
from server import app
from survey import *
from respond import respondent
from question import quest_tree,addQ,delQ,getQ


@app.route("/", methods = ["GET", "POST"])
#This isnt going to the login page first...
def index():
    s = survey()
    
    if request.method == "POST":
        #username = request.form["Username"]
        #password = request.form["Password"]
        return render_template("courselect.html", course_list=s.courselist())
    return render_template("main.html")

# survey creation in this controller
@app.route("/create_sur")
@app.route("/create_sur/<string:name>",methods=["GET","POST"])
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
            return render_template("finalsurvey.html", course_name=coursename, quest_list=s.coursequestionlist(coursename) )
        else:
            error = "please add at least one question for this survey."
    # teacher have select a course but not have select a question yet
    # getting all the question
    q_list = get_question.findQ()
    return render_template("surveycreate.html", course_name=name, quest_list=q_list, error = error)







@app.route("/student/<string:name>", methods=["GET", "POST"])
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
                error = "must finish the survey"
        print(answerlist)
        if not error:
            res.append_csv(answerlist)
            return render_template("finish_survey.html")

    return render_template("student.html", course_name = name, error = error, quest_list = questionlist,length = length)


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
    
    #Route to the results page displaying results of a survey.
    #not sure how the data csv's are setup or how it should know which csv to read
    @app.route("/results")
    def show_results():
        s = survey()
        if request.method == "GET":
            return render_template("results.html",res_list=get_results())
        return render_template("surveycreate.html", course_list = s.course_list())
    
    
    
    
    
    
    
    
    
    
    
    
