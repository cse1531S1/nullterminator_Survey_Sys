import csv
from survey import survey

class respondent():
    def __init__(self, coursename):
        self.coursename = coursename
        self.get_csv();

    def get_csv(self):
        # get an instance of survey to get the questionlist of this survey
        s = survey()
        question_list = s.coursequestionlist(coursename=self.coursename)
        self._length = len(question_list)
        self._question = question_list

    def append_csv(self, answerlist):
        with open('student/%s.csv' % self.coursename,'a') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow(answerlist)

    def get_length(self):
        return self._length

    def get_question(self):
        return self._question
        
    def get_results(self):
        results = []
     
        with open('student/%s.csv' % self.coursename, 'r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                results.append(row)
               
        return results 
