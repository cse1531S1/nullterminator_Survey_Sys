import csv


class survey:
## This funcation is used for creating a sample question list
## THe question structure is:[question_id, question,"answer1","answer2","answer3","..."]
    def question(self):
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
        
##This function is used to store the selected question to an coursequestion.csv file.
    def choosequestion(self,qid=[],coursename=""):
        with open('%s.csv' % coursename,'w+') as csv_out:
            writer = csv.writer(csv_out)
            all_question = self.question()
            for j in range(len(qid)):
                for i in range(len(all_question)):
                    if (i+1) == int(qid[j]):
                        print(all_question[i])
                        writer.writerow(all_question[i])



## for different question, I want to know how many answers it has
##so that I could print out their answer collectly.
##hence, this function will retirn a list[4,3,2], 
##because question1 has 4 answer, question2 has 3 answer,question3 has 2 answer.
    def list_number_of_answer(self,question_list):
        list_number_of_answer=[]
        for i in range(len(question_list)):
            list_number_of_answer.append(len(question_list[i])-2)
        print(list_number_of_answer)
        return list_number_of_answer
