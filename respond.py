import csv

Class respondent:
    def __init__(self, coursename):
        self.coursename = coursename
        
    def get_csv(self):
        with open('%s.csv' % self.coursename,'r') as csv_in:
        reader = csv.reader(csv_in)
        questionlist=[]
        for row in reader:
            questionlist.append(row)
    
    def append_csv(self):
        with open('student_%s.csv' % self.coursename,'a') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow(answerlist)
            
    
