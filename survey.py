import csv


class survey:

##This function is used to store the selected question to an coursequestion.csv file.
    def choosequestion(self,q_list=[],coursename=""):
        with open('%s.csv' % coursename,'w+') as csv_out:
            writer = csv.writer(csv_out)
            print(q_list)
            # i if the new order of each question
            i = 0
            for question in q_list:
                # increment the i and save the count into each question
                i+= 1
                question[0]= i
                # write the questions into csv files.
                writer.writerow(question)

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
