from sql_uti import SqlUtil
from user import UserData
from question import Question
from survey import Survey
import json

"""Two base class for the respond controller"""
class RespondMcq(SqlUtil):
    """Control table for respond_mcq."""
    def __init__(self):
        super().__init__("respond_mcq")
        self.__q = Question()
    def new_ans(self, respond_id,question_id, answer):
        # insert the respond_id by respond class
        self.insert("respond_id", respond_id)
        # insert the question_id
        self.insert("question_id", question_id)
        # insert the answer
        self.insert("answer", answer)
        return self.save()

    def count_respond(self, survey_id, question_id):
        # count grather all the respond to gether

        # get the information of this question
        this_q = self.__q.find_q(question_id)
        this_q = this_q[0]

        # count id for possible answers
        a_count = 0
        # to record all the answers
        ans_l = [this_q[1],this_q[2]]

        for q in this_q[3:]:
            # serach for all possible answers
            self.clear(join =True, col=True)

            # get the information of this question
            this_q = self.__q.find_by_id(question_id).one()

            # join table search
            self.with_table("respond","respond_id","id").col_name("answer")
            # find the criteria
            self.find("question_id",question_id).find("survey_id",survey_id)
            # answer filter
            self.find("answer",a_count)


            a_count +=1
            # count the answer number for this answer
            return_list = self.all()

            # count the results and append in to list
            ans_l.append([q,len(return_list)])

            # force clear all the join
            self.clear(True, True)

        # return [question,[[ans, count],..]]
        return ans_l

    def delete_by_respond_id(self, respond_id):
        self.find("respond_id", respond_id).delete()

class RespondText(SqlUtil):
    """Table control for respond_text"""
    def __init__(self):
        super().__init__("respond_text")
        self.__q = Question()
    def new_ans(self, respond_id,question_id, answer):
        # insert the respond_id by respond class
        self.insert("respond_id", respond_id)
        # insert the question_id
        self.insert("question_id", question_id)

        # insert the answer
        self.insert("answer", answer)
        return self.save()


    def count_respond(self, survey_id, question_id):
        # count grather all the respond to gether

        # get the information of this question
        this_q = self.__q.find_by_id(question_id).one()

        # join table search
        self.with_table("respond","respond_id","id").col_name("answer")
        # find the criteria
        self.find("question_id",question_id).find("survey_id",survey_id)

        # pop the first item in the list, and search that
        return_list = [this_q[1],this_q[2],[res[0] for res in self.all()]]
        # force clear all the join
        self.clear(True, True)
        # return [question, [all the answers]]
        return return_list

    def delete_by_respond_id(self, respond_id):
        self.find("respond_id", respond_id).delete()


class Respond(SqlUtil):
    """Controller for Respond, control the table for respond"""
    def __init__(self):
        super().__init__("respond")
        # two for inserting new respond
        self.__mcq = RespondMcq()
        self.__text = RespondText()
        # check the type of question
        self.__survey = Survey()
        self.__question = Question()
    def new_res(self, survey_id, user_id, answers):
        # getting of all the question id by order in the survey database
        this_q = self.__survey.get_qids(survey_id)
        if len(answers)!= len(this_q):
            print(this_q)
            print(len(answers),len(this_q))
            raise TypeError("The answer is not enough or Too much.")

        # create a new record for this respond
        self.insert("survey_id", survey_id)
        # store the student id who submit the survey
        self.insert("user_id",user_id)
        self.save()

        # getting back the respond_id that just inserted
        self.find(["survey_id","user_id"], [survey_id,user_id], sign = "=")
        respond_id = self.sort_by("id", ascdending = False).one()[0]

        for index in range(len(this_q)):
            # get the question type then try to put into correct respond
            this_type = self.__question.get_type(this_q[index])
            if this_type == "MCQ":
                self.__mcq.new_ans(respond_id,this_q[index], answers[index])
            elif this_type == "TEXT":
                self.__text.new_ans(respond_id,this_q[index], answers[index])

        return respond_id

    def delete_by_respond_id(self, respond_id):
        # find the respond that should delete
        self.find("id", respond_id).delete()

        # find the record of answer to delete
        self.__mcq.delete_by_respond_id(respond_id)
        self.__text.delete_by_respond_id(respond_id)

    def get_results(self, survey_id):
        # get all the results into an array to give back
        # getting all the question
        this_q = self.__survey.get_qids(survey_id)

        result_l = []

        for index in range(len(this_q)):
            # get the question type then try to put into correct respond
            this_type = self.__question.get_type(this_q[index])
            if this_type == "MCQ":
                result_l.append(self.__mcq.count_respond(survey_id,this_q[index]))
            elif this_type == "TEXT":
                result_l.append( self.__text.count_respond(survey_id,this_q[index]))

        return result_l
    def is_submitted(self, survey_id, uid):
        # check whether the user have submitted this survey
        if self.find(["survey_id","user_id"],[survey_id,uid]).one():
            return True
        return False

if __name__ == '__main__':
    # unitests
    res=Respond()
    this_id = []
    this_id .append( res.new_res(1, 2, ["1","I dont","15"]))
    this_id.append( res.new_res(1, 2, ["1","No need to improve","21"]))
    this_id .append(res.new_res(1, 2, ["1","I dont","18"]))

    print(res.all())

    # test the get_results fucntion is working
    print ("all the result currently have is")
    print(res.get_results(1))

    print("\nFound the result")
    s = RespondMcq()
    print()


    for rid in this_id:
        # delte the respond just create
        res.delete_by_respond_id( rid)

    # check whether the data have been stored
    print(res.all())
