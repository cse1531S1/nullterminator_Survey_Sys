from flask import Flask, redirect, render_template, request, url_for
from server import app
from survey import *
from respond import respondent
import csv


s = survey()


##THis function is being used when teacher click no question for their survey, and it could return a warning web page. 
@app.route("/coursepage/warning", methods=["GET", "POST"])
def warning():
    return("hey, please go back and add your answer!")




##THis function is used read in the generated coursequestion.csv file, and make it a courselist.
## after that, you could print out the coursequestionlist to show waht is your final survey 
@app.route("/coursepage/<string:coursename>/finalsurvey", methods=["GET", "POST"])
def finalsurvey(coursename):
    
    return render_template("finalsurvey.html", course_name=coursename, questionfield=s.coursequestionlist(coursename),length=len(s.coursequestionlist(coursename)), number_of_answer=s.list_number_of_answer(s.coursequestionlist(coursename)) )      




##first, it will show all the question have been created.
##Then, teacher chooses his desired questions
##All the questions being chosen will be used to create a csv file
## if no question chosen, it won't create csv file.
@app.route("/addquestions/<string:coursename>", methods=["GET", "POST"])
def addquestions(coursename):
    if request.method == "POST":
        selected_q = request.form.getlist("check_list[]") 
        if selected_q != []:
            s.choosequestion(selected_q,coursename) #create a csv file
            return redirect(url_for('finalsurvey',coursename=coursename))
        else:
            return redirect(url_for('warning'))
##The return statement of function question() is the list of all the questions         
    return render_template("surveycreate.html", course_name=coursename, questionfield=s.question(),length=len(s.question()), number_of_answer=s.list_number_of_answer(s.question()) )





##THis is the function to show all the course
##The return statement of function course() is the list of all the function 
@app.route("/selectcourse", methods=["GET", "POST"])
def course_adding():
   
    if request.method == "POST":
        return redirect(url_for('addquestions', coursename=request.form["co"]))
 
    courselist = s.courselist()
    return render_template("courselect.html", course=courselist, length=len(courselist) )



@app.route("/student/<string:coursename>", methods=["GET", "POST"])
def student(coursename):
    res = respondent(coursename)
    error = None
    length = res.get_length()
    questionlist = res.get_question()
    
    if request.method == "POST":
        answerlist = []
        for i in range(length):
            try:
                answerlist.append(request.form[str(i)])
            except :
                error = "must finish the survey"
                
        if not error:
            res.append_csv(answerlist)
            return render_template("finish_survey.html")
    
    return render_template("student.html", course_name = coursename, error = error, questionfield = questionlist,length = length, number_of_answer = s.list_number_of_answer(questionlist))
