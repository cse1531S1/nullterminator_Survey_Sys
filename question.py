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
        return new_node

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

    def push_buffer(cls,node):
        cls.buffer_obj.append(node)
    def __init__(self):
        super(quest_tree, self).__init__()
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
                    # try to search the for the valid question.
                    return_list.append(cls._questDisct[int(i)].getlist() )
                except KeyError:
                    print ("fail on find question", i)
            return return_list

    def get_new_id(cls):
        # assign a new id to return
        cls.max_id +=1
        return cls.max_id


    def add_question(cls,question = "", answers = []):
        if len(answers)<2 or question == "":
            # fail to create the question
            return 0
        # else:
        # give the new question a new id, add quesitons and answers in the list
        row = [cls.max_id+1,question]
        for answer in answers:
            row.append(answer)

        # add it into the dict
        new_node = cls.csv_readRow(row)
        # add it into buffer to be adding to csv
        cls.buffer_obj.append(new_node)
        return 1

    def delete_question(cls, question_id):
        try:
            # delet the record in the in self dictionary
            del cls._questDisct[int (question_id)]
            # successfully delete question
            return 1
        except KeyError:
            print("Fail on delet question", question_id)
            return 0

class delQ():
    def __init__(self, qTree):
        self._qTree = qTree
    def doDel(self,qID=[]):
        if len(qID)!= 0:
            # if qid != None hence do the delete
            for qid in qID:

                self._qTree.delete_question(int(qid))
            # write the change into the csv file
            csv_util.write_csv(self._qTree)

class getQ():
    """docstring for getQuestion."""
    def __init__(self,qTree):
        super(getQ, self).__init__()
        # keep an instance of the question_tree.
        self._qTree = qTree
    def findQ(self,qId = None):
        return_list = self._qTree.find_question(qId)
        if len(return_list) ==0:
            # return none obj, to better template use
            return None
        # else:
        return return_list
class addQ():
    """docstring for addQuestion."""
    def __init__(self, quest_tree):
        # super(addQuestion, self).__init__()
        self._qTree =quest_tree
    def is_valid_Q(self,question = "", answers = []):
        if len(question)<= 0:
            return "question has not define"
        if len(answers) <2:
            return "answer is not enough"
        return 0
    def add_Q(self, question = "", answers = []):
        if self.is_valid_Q(question, answers)== 0:
            # valid question
            # try to assign a new queston id for this question
            this_id = self._qTree.get_new_id()
            # put all the information into a list
            row = [this_id,question]
            for answer in answers:
                row.append(answer)

            # translate the list into node and assign this question into dictionary
            q_node=self._qTree.csv_readRow(row)
            # push this node to be write
            self._qTree.push_buffer(q_node)
            csv_util.append_csv(self._qTree)


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


    # print("try to add the question into the file")
    # quests.add_question("q3",["q3a0","q3a1"])
    # # write the new question into the csv
    # csv_util.append_csv(quests)

    quests2 = quest_tree()
    print ("find the question with a new class")
    quest_find  = getQ(quest_tree())
    print(quest_find.findQ([1,0,3]))

    question_add = addQ(quests2)
    question_add.add_Q("q3",["q3a0","q3a1"])


    #test function for delete_question
    qDel = delQ(quests2)
    # couldn't delete the question while flying
    #qDel.doDel([5])
