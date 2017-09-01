from flask import Flask, redirect, render_template, request, url_for
from math import sqrt, sin, cos, tan, log
from server import app
import csv

emptystring=""
user_input=""

def course():
    with open('courses.csv','r') as csv_in:
        reader = csv.reader(csv_in)
        courselist=[]
        for row in reader:
            courselist.append(row)
    del courselist[0]
    return courselist

def question():
    # test caset question list
    question_list=[
        [0,"what is your name?","A. hugo","B. ruofei","C.daniel","D.hendri"],
        [1,"what is your favorite fruit?","A. apple","B. banana","C. rockmelon"],
        [2,"what is your favorite color?","A. red","B. blue"]
    ]
    # print(question_list)
    return question_list

def list_number_of_answer(question_list):
    answer_number_list=[]
    for i in question_list:
        answer_number_list.append(len(i)-2)
    #print(answer_number_list)
    return answer_number_list

def storedquestion(qid=[],coursename=""):
    print(qid)
    with open('%s.csv' % coursename,'w+') as csv_out:
        writer = csv.writer(csv_out)
        all_question = question()
        for j in range(len(qid)):
            for i in range(len(all_question)):
                if (i+1) == int(qid[j]):
                    print(all_question[i])
                    writer.writerow(all_question[i])

@app.route("/coursepage/<string:coursename>/studentsurvey", methods=["GET", "POST"])
def student_part(coursename=""):
    with open('%s.csv' % coursename,'r') as csv_in:
        reader = csv.reader(csv_in)
        courselist=[]
        for row in reader:
            courselist.append(row)
    return courselist

@app.route("/coursepage/<string:coursename>/finalsurvey", methods=["GET", "POST"])
def finalsurvey(coursename):
    with open('%s.csv'% coursename,'r') as csv_in:
        reader = csv.reader(csv_in)
        questionlist=[]
        for row in reader:
            questionlist.append(row)
        print(questionlist)
    return render_template("finalsurvey.html", course_name=coursename, questionfield=questionlist,length=len(questionlist), number_of_answer=list_number_of_answer(questionlist) )

@app.route("/coursepage/<string:coursename>", methods=["GET", "POST"])
def coursepage(coursename):
    if request.method == "POST":
        selected_q = request.form.getlist("check_list[]")
        storedquestion(selected_q,coursename) #create a csv file
        return redirect(url_for('finalsurvey',coursename=coursename))
    return render_template("surveycreate.html", course_name=coursename, questionfield=question(),length=len(question()), number_of_answer=list_number_of_answer(question()) )

@app.route("/selectcourse", methods=["GET", "POST"])
def course_adding():
    if request.method == "POST":
        return redirect(url_for('coursepage', coursename=request.form["co"]))
    return render_template("courselect.html", course=course(), length=len(course()) )

@app.route("/student/<string:coursename>", methods=["GET", "POST"])
def student(coursename):
    error = None
    with open('%s.csv'% coursename,'r') as csv_in:
        reader = csv.reader(csv_in)
        questionlist=[]
        for row in reader:
            questionlist.append(row)
    if request.method == "POST":
        answerlist = []
        for i in range(len(questionlist)):
            try:
                answerlist.append(request.form[str(i)])
            except :
                error="you must have to finish the survey"
                
        with open('student_%s.csv'%coursename,'a') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow(answerlist)
        return render_template("finish_survey.html")
    return render_template("student.html", course_name=coursename,error = error, questionfield=questionlist,length=len(questionlist), number_of_answer=list_number_of_answer(questionlist))
