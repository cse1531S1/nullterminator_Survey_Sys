import csv

class survey:
    ##This function is used to store the selected question to an coursequestion.csv file.
    def choosequestion(self,q_list=[],coursename=""):
        with open('%s.csv' % coursename,'w+') as csv_out:
            writer = csv.writer(csv_out)
            # i if the new order of each question
            i = 0
            for question in q_list:
                # increment the i and save the count into each question
                i+= 1
                question[0]= i
                # write the questions into csv files.
                writer.writerow(question)

    ## Given a course name, return all the questions store in the file
    def coursequestionlist(self,coursename=""):
        with open('%s.csv'% coursename,'r') as csv_in:
            reader = csv.reader(csv_in)
            coursequestionlist=[]
            for row in reader:
                ## read out all the questions
                coursequestionlist.append(row)
        ## return all questions that read
        return coursequestionlist

    ## read in a courselist csv file
    ## put all the course names in to courselist
    def courselist(self):
        # list for storing all the course
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
        	
    def get_results():
        results = []
        def read():
            with open('data.csv', 'r') as csv_in:
                reader = csv.reader(csv_in)
                for row in reader:
                    results.append(row)
        return results 
    
    


if __name__ == '__main__':
    sur = survey()
    print (sur.courselist())
