from db.sql_uti import SqlUtil

class Answer(SqlUtil):
    """docstring for Answer."""
    def __init__(self):
        super().__init__("answer")

    def find_by_qid(self, q_id):
        self.find("q_id",int(q_id))
        return self
    def find_a(self, q_id):
        if type(q_id) in [str,int]:
            ans_list = self.find_by_qid(q_id).all()
            return [ans[2] for ans in ans_list]
        else:
            raise TypeError("Question id must be int or str.")
    def add_a(self, answers, q_id):
        if type(answers)== list and len(answers) >=2 and type(q_id) in [str,int]:
            # valid type for adding a question
            for a in answers:
                # append all the answers into database system
                self.insert(["q_id","answer"],[q_id,a]).save()
        else:
            # try to handle the error by raise different error msg
            if type(answers) != list:
                raise TypeError("Answers must be a list.")
            if len(answers) < 2:
                raise TypeError("A question must have at lease 2 answers.")
            if not type(q_id) in [str,int]:
                raise TypeError("Code Error: q_id is not a str or int")
    def del_a(self, q_id):
        if not type(q_id) in [str, int]:
            raise TypeError("Question id must be int or str.")
        self.find_by_qid(q_id).delete()

class Question(SqlUtil):
    """docstring for Question."""
    def __init__(self):
        super().__init__("question")
        # create an instance of answer to append answer table
        self.__ans = Answer()
        # set up the defualt search column
        self.clear()

    def clear(self, join = False, col = False):
        # overwrite the father function to set up default in __from
        super().clear(join,True)
        if not col:
            # reset the col value
            # in default only two column would show
            self.col_name(["id","question"])


    def find_by_id(self,q_id):
        # convent function in complement of sql_util
        self.find("id",int(q_id))
        return self


    def find_q(self, q_id=None, pool_id = None):
        # default situation would show up all the hidden question
        return_list = []
        if  not q_id:
            if not pool_id:
                raise TypeError("pool_id must specify while getting all avaliable question")
            if not type(pool_id) in [str, int] :
                # couldn't handle else of these two type
                raise TypeError("Code Error: pool_id must be int or str")
            # q_id == None
            # return all the avaliable question (show = 1)
            return_list = self.find("show", 1)\
                            .find("pool_id",int(pool_id)).all()
            # return all the questions and with its' answers
            return [q+self.__ans.find_a(q[0]) for q in return_list]

        elif type(q_id) == list:
            for q in q_id:
                # collect all the return
                return_list.append(self.find_q(q))
            return return_list
        elif type(q_id) in [str,int]:
            return_list = self.find_by_id(q_id).one()
            # get all the answers append at the end of each question
            return [q+self.__ans.find_a(q[0]) for q in return_list]
        else:
            # couldn't hand this type
            raise TypeError("Question id must be a list or string or interger")
    def add_q(self, answers, question,pool_id):
        # error handling
        if not (type(answers)== list and len(answers)>=2 and \
            type(pool_id) in [str,int] and type(question) == str):
            if type(answers) != list:
                raise TypeError("Answers must be a list.")
            if len(answers) < 2:
                raise TypeError("A question must have at lease 2 answers.")
            if not type(pool_id) in [str,int]:
                raise TypeError("Code Error: pool_id is not a str or int.")
            if type(question) != str:
                raise TypeError("A question must be a string.")

        # valid question and answers
        self.insert(["question","pool_id"],[question,int(pool_id)]).save()
        # get the q_id for the question just created
        # by getting the newest record that have same property
        this_q = self.find(["question","pool_id"],[question,int(pool_id)])\
                    .sort_by("id",False).one()
        q_id = this_q[0]
        # call the class Answer to append this question's answers
        self.__ans.add_a(answers,q_id)

        # for convience return the q_id for just created question
        return q_id
    def del_q(self, q_id):
        self.find_by_id(q_id).delete()
        self.__ans.del_a(q_id)
        return self
if __name__ == '__main__':
    quest = Question()
    # add a test question into database
    this_id=quest.add_q(["a1","a2"], "sample question?", "0")

    # getting all the question in the database with pool_id = 0
    print(quest.find_q(pool_id="0"))

    # delete the question we just create for test
    quest.del_q(this_id)

    # check whether it's successfully deleted
    print(quest.find_q(pool_id="0"))
