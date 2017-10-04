from sql_uti import SqlUtil
from server import app

class Respond(SqlUtil):
    """docstring for respond."""
    def __init__(self):
        super().__init__("respond")
    def find_by_surveyID(self, survey_id):
        if not type(survey_id) in [int,str]:
            raise TypeError("ID from survey must be a integer")
        # simple case of mapping a function to dynamic execute SQL
        return self.find("id",int(survey_id)).one()
    def insert_response(self,survey_id,uid):
        return self.insert(["survey_id","uid"],[survey_id,uid]).save()
    def get_respond(self,survey_id):
        this_respond = self.find("survey_id",survey_id)\
                        .find("uid",uid).one()
        return this_course()
    def delete_respond(self,id):
        if type(id)!= int:
            raise TypeError("input id must be int")
        self.find("id",id).delete()

class RespondMCQ(SqlUtil):
    """docstring for res_mcq"""
    def __init__(self):
        super().__init__("res_mcq")
    def find_by_resID(self,respond_id):
        if not type(respond_id) in [int,str]:
            raise TypeError("ID from respond must be a integer")
        # simple case of mapping a function to dynamic execute SQL
        return self.find("id",int(respond_id)).one()
    def insert_res_mcq(self,respond_id,ans_list):
        return self.insert("respond_id",respond_id).insert("ans_list","&&".join(ans_list)).save()
        
class RespondText(SqlUtil):
    """docstring for res_text"""
    def __init__(self):
        super().__init__("res_text")
    def find_by_resID(self,respond_id):
        if not type(respond_id) in [int,str]:
            raise TypeError("ID from respond must be a integer")
        # simple case of mapping a function to dynamic execute SQL
        return self.find("id",int(respond_id)).one()
    def insert_res_text(self,respond_id,ques_id,answer):
        return self.insert(["respond_id","ques_id","answer"],[respond_id,ques_id,answer]).save()
        
class RespondController():
    def __init__(self):
        self.__respond = Respond()
        self.__res_mcq = RespondMCQ()
        self.__res_text = RespondText()
        
if __name__ == '__main__':
    res = Respond()
    res.test_exe().insert_response(1,50)
    print(res.get_respond)
    res.delete_respond(1)
    print(res.get_respond)
