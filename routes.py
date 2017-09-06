from flask import Flask, redirect, render_template, request, url_for
from server import app
import csv




## read in the courses.csv file and put all the courses into courselist 
def course():
    with open('courses.csv','r') as csv_in:
        reader = csv.reader(csv_in)
        courselist=[]
        newrow=""
        for row in reader:
            newrow=''.join(row)
            courselist.append(newrow)
    del courselist[0]
    courselist.pop()
    return courselist




## This funcation is used for creating a sample question list
## THe question structure is:[question_id, question,"answer1","answer2","answer3","..."]
def question():
    question_list=[]
    question_number0=1
    question0="what is your name?"
    single_question0=[question_number0,question0,"A. hugo","B. ruofei","C.daniel","D.hendri"]

    question_number1=2
    question1="what is your favorite fruit?"
    single_question1=[question_number1,question1,"A. apple","B. banana","C. rockmelon"]

    question_number2=3
    question2="what is your favorite color?"
    single_question2=[question_number2,question2,"A. red","B. blue"]

    question_list.append(single_question0)
    question_list.append(single_question1)
    question_list.append(single_question2)
    print(question_list)
    return question_list



## for different question, I want to know how many answers it has
##so that I could print out their answer collectly.
##hence, this function will retirn a list[4,3,2], 
##because question1 has 4 answer, question2 has 3 answer,question3 has 2 answer.
def list_number_of_answer(question_list):
    list_number_of_answer=[]
    for i in range(len(question_list)):
        list_number_of_answer.append(len(question_list[i])-2)
    print(list_number_of_answer)
    return list_number_of_answer
 


##This function is used to store the selected question to an coursequestion.csv file.
def storedquestion(qid=[],coursename=""):
    print(qid)
    
    all_question = question()
    for j in range(len(qid)):
        for i in range(len(all_question)):
            if (i+1) == int(qid[j]):
                print(all_question[i])
                writer.writerow(all_question[i]) 



##THis function is being used when teacher click no question for their survey, and it could return a warning web page. 
@app.route("/coursepage/warning", methods=["GET", "POST"])
def warning():
    return("hey, please go back and add your answer!")



##THis function is used read in the generated coursequestion.csv file, and make it a courselist.
## after that, you could print out the coursequestionlist to show waht is your final survey 
@app.route("/coursepage/<string:coursename>/finalsurvey", methods=["GET", "POST"])
def finalsurvey(coursename):
    with open('%s.csv'% coursename,'r') as csv_in:
        reader = csv.reader(csv_in)
        coursequestionlist=[]
        for row in reader:
            coursequestionlist.append(row)
        ##print(questionlist)
    return render_template("finalsurvey.html", course_name=coursename, questionfield=coursequestionlist,length=len(coursequestionlist), number_of_answer=list_number_of_answer(coursequestionlist) )      
with open('%s.csv' % coursename,'w+') as csv_out:
        writer = csv.writer(csv_out)


##first, it will show all the question have been created.
##Then, teacher chooses his desired questions
##All the questions being chosen will be used to create a csv file
## if no question chosen, it won't create csv file.
@app.route("/coursepage/<string:coursename>", methods=["GET", "POST"])
def coursepage(coursename):
    if request.method == "POST":
        selected_q = request.form.getlist("check_list[]") 
        if selected_q != []:
            storedquestion(selected_q,coursename) #create a csv file
            return redirect(url_for('finalsurvey',coursename=coursename))
        else:
            return redirect(url_for('warning'))
##The return statement of function question() is the list of all the questions         
    return render_template("surveycreate.html", course_name=coursename, questionfield=question(),length=len(question()), number_of_answer=list_number_of_answer(question()) )


##THis is the function to show all the course
##The return statement of function course() is the list of all the function 
@app.route("/selectcourse", methods=["GET", "POST"])
def course_adding():
   
    if request.method == "POST":
        return redirect(url_for('coursepage', coursename=request.form["co"]))
    return render_template("courselect.html", course=course(), length=len(course()) )








#Display page of results for a particular course
#unfinished -- 
@app.route("/show_results", methods=["GET", "POST"])
def show_results(coursename):
    if request.method == "POST":
        return redirect(url_for('resultspage', resultList=request.form["results"]))
    return render_template("course_results.html", resultlist=get_results(), length=len(results()), course=coursename )
	
def get_results():
    results = {}
    def read():
        with open('data.csv', 'r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                results.append(row)
        return results	










