import csv

class question():
    """docstring for question."""
    # allocate the location of the csv file

    # a dict to store all the instance of this object
    _questDisct = {}

    def __str__(slef):
        # print this class
        string = ""
        if slef.id:
            string = str(self.id )+ str(self.question)+str(self.answers)
            return string
        return "this is a tree object"


    def get_csvName(cls):
        return "question.csv";

    def __init__(self, row= None):
        # super(question, self).__init__()
        if row != None:
            # initialise for node object
            self.id = int(row[0])
            self.question =str(row[1])
            self.answers = row[2:] # grep all the things after three

            # assing this item into the diction to prepare searching
            _questDisct[self.id]= self
        else:
            # this obj act like a tree object

            pass

    def csv_readRow(row):
        # try to read each row in this function
        # after reading a row add an instance of this class into the _questDisct
        # data_struct is: id, question, [answers]..

        # create the new item to append
        new =  question(row)

    def csv_writeRow():
        return_array =[]
        for key,values in _questDisct:
            return
        return return_array

    def find_question(ques_id = None):
        if ques_id == None:
            # no input values, return all the values back
            return _questDisct.values()
        else :
            # input some things
            return_list = []
            for i in ques_id:
                # searching all the given values
                return_list.append(_questDisct[i] )
            return return_list

# class myCSV():
#     """docstring for myCSV."""
#     def __init__(self):
#         pass

def write(obj):
    with open("question.csv",'a') as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(obj.csv_writeRow())
    # pass
def read(obj):
    with open(obj.get_csvName(),'r') as csv_in:
        reader = csv.reader(csv_in)
        for row in reader:
            # calling back the passed in obj to deal with the csv
            obj.csv_readRow(row)




if __name__ == '__main__':
    # unittests
    # ques = question()
    write(question.get_csvName());
    # this_survey = survey('1511-17s1')
    # 1.q1
    # 2.q2
    # 3.q3
    # [
    #     [1,q1,answers]
    #     [2,q2,answers]
    # ]
    # this_survey.add_question()
    #
    # question.find_question([1,2])
