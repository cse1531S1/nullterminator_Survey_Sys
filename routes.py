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
    question_list=[]
    question_number0=1
    question0="what is your name?"
    answer0=["A. hugo","B. ruofei","C.daniel","D.hendri"]
    single_question0=[question_number0,question0,answer0]

    question_number1=2
    question1="what is your favorite fruit?"
    answer1=["A. apple","B. banana","C. rockmelon" ]
    single_question1=[question_number1,question1,answer1]

    question_number2=3
    question2="what is your favorite color?"
    answer2=["A. red","B. blue" ]
    single_question2=[question_number2,question2,answer2]

    question_list.append(single_question0)
    question_list.append(single_question1)
    question_list.append(single_question2)
    return question_list

def list_number_of_answer(question_list):
    list_number_of_answer=[]
    for i in range(len(question_list)):
        list_number_of_answer.append(len(question_list[i][2]))
    print(list_number_of_answer)
    return list_number_of_answer
 

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





