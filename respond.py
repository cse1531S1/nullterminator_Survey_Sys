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

    def get_open_course(self):
        s =survey()
        open_course = []
        for course in s.courselist():
            try:
                open("student/%s.csv" % course , mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True)
                open_course.append(course)
            except:
                pass
        return open_course
    def get_results(self):
        data = []
        # get an instance of survey to get the questionlist of this survey
        s = survey()
        question_list = s.coursequestionlist(coursename=self.coursename)

        with open('student/%s.csv' % self.coursename, 'r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                data.append(row)

        results = []
        question_no = 0
        for question in question_list:
            # for every question
            append_list = [question[0],question[1]]
            i = 0
            for answer in question[2:]:
                collect = 0
                for j in range(len(data)):
                    # search for all respond of this question for answer i
                    if int(data[j][question_no]) == i:
                        collect+=1
                append_list.append([answer,collect])
                i +=1
            # append the answer+ results list into the results
            results.append(append_list)
            append_list = []
            # question_no add one
            question_no+=1


        return results
