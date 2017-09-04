import csv

class respondent():
    def __init__(self, coursename):
        self.coursename = coursename
        self.get_csv();
        
    def get_csv(self):
        with open('%s.csv' % self.coursename,'r') as csv_in:
            reader = csv.reader(csv_in)
            questionlist=[]
            for row in reader:
                questionlist.append(row)
        self._length = len(questionlist)
        self._question = questionlist
    
    def append_csv(self, answerlist):
        with open('student_%s.csv' % self.coursename,'a') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow(answerlist)
            
    def get_length(self):
        return self._length
    
    def get_question(self):
        return self._question
