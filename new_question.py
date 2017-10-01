from sql_uti import SqlUtil
from server import app

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
            self.col_name(["id","question","type"])


    def find_by_id(self,q_id):
        if not type(q_id) in [str,int]:
            raise TypeError("q_id must be a int or str")

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
            return_list = self.find("show", 1).find("show",1)\
                            .find("pool_id",pool_id).all()
            # return all the questions and with its' answers
            return [q+self.__ans.find_a(q[0]) for q in return_list]

        elif type(q_id) == list:
            for q in q_id:
                # collect all the return
                return_list+=self.find_q(q)
            return return_list
        elif type(q_id) in [str,int]:
            this_q = self.find_by_id(int(q_id)).one()
            if this_q[2] in ["MCQ"]:
                # get all the answers append at the end of each question
                return [this_q+self.__ans.find_a(this_q[0])]
            elif this_q[2] in ["TEXT"]:
                # Text base question don't have answers to specify
                return [this_q]
            else:
                raise TypeError("Code Error: Counldn't handle this type of question:",this_q[2])

        else:
            # couldn't hand this type
            raise TypeError("Question id must be a list or string or interger")

    def add_q(self,question,pool_id, q_type,answers = None):
        # error handling
        if not (type(pool_id) in [str,int] and len(question)>0 and type(question) == str and \
            q_type in ["MCQ","TEXT"]):

            if not type(pool_id) in [str,int]:
                raise TypeError("Code Error: pool_id is not a str or int.")
            elif len(question)==0:
                raise TypeError("Question must be specify.")
            elif type(question) != str:
                raise TypeError("A question must be a string.")
            elif not q_type in ["MCQ","TEXT"]:
                raise TypeError("unknown q_type: ", q_type)

        if q_type != "TEXT":
            if type(answers) != list:
                raise TypeError("Answers must be a list.")
            if len(answers) < 2:
                raise TypeError("A question must have at lease 2 answers.")
        # valid question and answers
        self.insert(["question","pool_id","type"],[question,int(pool_id),q_type]).save()
        # get the q_id for the question just created
        # by getting the newest record that have same property
        this_q = self.find(["question","pool_id","type"],[question,int(pool_id),q_type])\
                    .sort_by("id",False).one()
        q_id = this_q[0]


        if q_type in ["MCQ"]:
            # only the MCQ base question would need some answer
            # call the class Answer to append this question's answers
            self.__ans.add_a(answers,q_id)

        # for convience return the q_id for just created question
        return q_id

    def quote_q(self, q_ids):
        # return all the question specify by q_ids and add a link count for each question
        if type(q_ids) != list:
            # error manage
            raise TypeError("q_ids must be a list")


        for q in q_ids:
            # to select the linked time
            self.clear(col= True)
            self.col_name("link")

            # all the linked time add one
            linked = self.find_by_id(q).one()
            self.update("link",linked[0]+1).find_by_id(q).save()
        q_list = self.find_q(q_ids)


        # return all the required question
        return q_list

    def del_q(self, q_id,force=False):
        if not type(q_id) in [list, str, int]:
            raise TypeError("Question should be deleted by Id of list of ids")

        if not q_id:
            raise TypeError("Delect question must be specify.")

        if type(q_id)  == list:
            for q in q_id:
                # recursively calling all the question's id
                self.del_q(q,force)

        else:
            # the input type is a str or int
            this_q = self.col_name("link").find_by_id(q_id).one()

            if this_q == None:
                # this_q has already deleted
                raise TypeError("The specify question is not exist in database.")
            if (this_q[0] ==0) or force:
                # delete the question by specify question id
                self.find_by_id(q_id).delete()
                # delete the question's answer
                self.__ans.del_a(q_id)
            else:
                # this question has been linked to some survey, couldn't delete
                # but unshow it
                self.find_by_id(q_id).update("show", 0).save()


        return self

if __name__ == '__main__':

    with app.app_context():
        quest = Question()
        # add a test question into database
        first_id=quest.add_q("sample question?", "0", "MCQ",["a1","a2"])
        second_id=quest.add_q( "sample question?", "0", "MCQ",["a1","a2"])
        third_id=quest.add_q( "sample question?", "0", "TEXT")



        print("try to find all the quesiton with question pool 0")
        # getting all the question in the database with pool_id = 0
        print(quest.find_q(pool_id="0"))


        list_q = [first_id,second_id,third_id]
        # pretend these selected question has been added to a survey
        print ("\nTry to queote added question into a survey")
        print(quest.quote_q(list_q))


        quest.col_name("link")
        print("\nTry to check the linked time for each question.")
        # check whether these question has been selected
        print(quest.find_q(list_q))


        print("\nDelete all the questions created for survey.")
        # delete the question we just create for test
        quest.del_q(list_q)

        # delete all the question in database
        # quest.del_q(list(range(1,81,1)),True)

        # check whether it's successfully deleted
        print(quest.find_q(pool_id="0"))

        # force delete all the question for test
        quest.del_q(list_q,True)
