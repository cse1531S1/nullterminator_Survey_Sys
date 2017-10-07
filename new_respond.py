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
