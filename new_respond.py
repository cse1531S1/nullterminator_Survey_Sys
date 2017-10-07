from sql_uti import SqlUtil
from server import app

class Respond(SqlUtil):
    """docstring for respond."""
    def __init__(self):
        super().__init__("respond")
    
    def get_response_course_qid(self,course_id,q_id):
        return self.find("course_id",course_id).find("q_id",q_id).all()
    
    def get_all_response_by_course(self,course_id):
        return self.find("course_id",course_id).all()
    
    def insert_response(self,course_id,q_id,answer):
        return self.insert(["course_id","q_id","answer"],[course_id,q_id,answer]).save()

    def delete_response_by_id(self,id):
        self.find("id",id).delete()

    def delete_all_response_by_course(self,course_id):
        self.find("course_id",course_id).delete()

    def delete_all(self):
        self.delete()

    def get_all(self):
        return self.all()

class User_respond(SqlUtil):
    def __init__(self):
        super().__init__("user_respond")
    
    def record_user_complete_survey(self,uid,courseid):
        return self.insert(["uid","courseid"],[uid,courseid]).save()
    
    def delete_user_record(self,uid):
        self.find("uid",uid).delete()
    
    def show_completed_by_user(self,uid):
        return self.find("uid",uid).all()

    def show_all_completed(self):
        return self.all()

    def delete_by_user(self,uid):
        self.find("uid",uid).delete()

    def delete_all(self):
        self.delete()

if __name__ == '__main__':
    res = Respond()
    res.insert_response(1,1,"abc")
    print(res.get_response_course_qid(1,1))
    res.delete_response_by_id(1)
    res.insert_response(1,1,"bcd")
    res.insert_response(1,1,"cde")
    print(res.get_all_response_by_course(1))
    res.delete_all_response_by_course(1)
    print(res.get_all_response_by_course(1))
    user = User_respond()
    user.record_user_complete_survey(50,1)
    print(user.show_completed_by_user(50))
    user.delete_all()
    print(user.show_all_completed())
    res.insert_response(1,1,"abc")
    res.insert_response(1,1,"bcd")
    res.insert_response(1,1,"cde")
    print(res.get_all())
    res.delete_all()
    print(res.get_all())
