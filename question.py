from csv_uti import csv_util

class quest_tree():
    """docstring for question."""
    # allocate the location of the csv file

    # a dict to store all the instance of this class's node
    _questDisct = {}
    max_id = 0
    buffer_obj = []

    def __str__(slef):
        # print this class
        string = ""
        if slef.id:
            string = str(self.id )+ str(self.question)+str(self.answers)
            return string
        return "this is a tree object"


    def csv_name(cls):
        return "question.csv";

    def csv_readRow(cls,row):
        # try to read each row in this function
        # after reading a row add an instance of this class into the _questDisct
        # data_struct is: id, question, [answers]..


        this_id = int(row[0])
        # try to refresh the max_id
        if this_id> quest_tree.max_id:
            quest_tree.max_id = this_id
        # use the row info to start a new row
        new_node = quest_node(this_id, row[1],row[2:])
        # assing this question node into the dictionary to be search
        quest_tree._questDisct[this_id] = new_node


    def csv_append(cls):
        # append the content at the end of the csv
        return_list = [item.getlist() for item in cls.buffer_obj]
        # clear the buffer
        buffer_obj = []
        # return the info should be append
        return return_list

    def csv_content(cls):
        # rewrite all the row in the csv file
        return cls.find_question();

    def __init__(self):
        # super(question, self).__init__()
        if quest_tree.max_id ==0:
            # initialize the class
            csv_util.read_csv(self)
        else:
            # class has been initialized
            pass

    def find_question(cls,ques_id = None):
        if ques_id == None:
            # no input values, return all the values back
                return [item.getlist() for item in cls._questDisct.values()]
        else :
            # input some things
            return_list = []
            for i in ques_id:
                # searching all the given values
                try:

                    return_list.append(cls._questDisct[i].getlist() )
                except KeyError:
                    print ("fail on find question", i)
            return return_list

    # def add_question(cls,question = "", answers = []):
    #     if len(answers)==0 || question == "":
    #         # invalid input



class quest_node():
    """docstring for quest_node."""
    def __init__(self, id, question = "", answers = []):
        super(quest_node, self).__init__()
        if question == "" or answers ==[]:
            # invalid initialise
            return None
        # else:
        # id must be an integer
        self.id = int(id);
        self.quest = question;
        self.answers = answers;

    def getlist(self):
        return_list = [self.id, self.quest]
        for i in self.answers:
            # append all the question in the return_list
            return_list.append(i)
        return return_list

    def __str__(self):
        # printing string generator
        string = str(self.id)+" "+self.quest+" "
        answers = ",".join(self.answers)
        return string+answers

if __name__ == '__main__':
    # unittests
    quests= quest_tree()
    # test the searching method
    this_quest_list = quests.find_question([1,0,3])
    for this in this_quest_list:
        print(this)


    this_quest_list = quests.find_question()
    for this in this_quest_list:
        print(this)
