import csv


class survey:

##This function is used to store the selected question to an coursequestion.csv file.
    def choosequestion(self,q_list=[],coursename=""):
        with open('%s.csv' % coursename,'w+') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow(q_list)



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


## Given a course name, go get a related coursequestion csv file
## read out all the questions
## put it into a coursequestionlist
    def coursequestionlist(self,coursename=""):
        with open('%s.csv'% coursename,'r') as csv_in:
            reader = csv.reader(csv_in)
            coursequestionlist=[]
            for row in reader:
                coursequestionlist.append(row)
        return coursequestionlist


## read in a courselist csv file
## put all the course names in to courselist
    def courselist(self):
        courselist=[]
        with open('courses.csv','r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                # append all the course name into the course list to return
                courselist.append(row[0])
        if len(courselist) == 0:
            # special usecase to return the None obj to template
            return None
        return courselist


if __name__ == '__main__':
    sur = survey()
    print (sur.courselist())
