from sql_uti import SqlUtil
from server import app
class Course(SqlUtil):
    """docstring for Course."""
    def __init__(self):
        super().__init__("course")

    def get_course(self,course_code=None,course_year=None):
        if course_code and course_year:
            this_course = self.find("course_code",course_code)\
                            .find("course_year",course_year).one()            
            return this_course
        return self.all()

class Survey(SqlUtil):
    """docstring for survey."""
    def __init__(self):
        super().__init__("survey")
        self.__course = Course()
    def create_survey(self,course_name,course_year,Q_id,start_time,end_time):
        #this_course_id = self.__course.get_course_id(course_code,course_year)
        self.insert("course_name",course_name).insert("course_year",course_year)\
                        .insert("Q_id","&&".join(Q_id))\
                        .insert("start_time",start_time)\
                        .insert("end_time",end_time).save()
        this_survey = self.find(["course_name","course_year","Q_id","start_time","end_time"],\
                        [course_name,course_year,"&&".join(Q_id),start_time,end_time])\
                        .sort_by("id",False).one()
        return this_survey[0]
    def get_survey(self,course_name,course_year):
        
        return self.find(["course_name","course_year"],[course_name,course_year]).one()

               
    def post_sur_to_staff(self,course_name,course_year):
   
        # post survey to related staff, stage = review
        this_survey = self.find(["course_name","course_year"],[course_name,course_year]).update("status",1).save()
        this_survey = self.find(["course_name","course_year"],[course_name,course_year]).one()
        return this_survey

    def delete_survey(self,id):
        if type(id)!= int:
            raise TypeError("input id must be int")
        self.find("id",id).delete()



if __name__ == '__main__':
    with app.app_context():
      course = Course()
      print(course.get_course("COMP1521","17s2"))
      survey = Survey()
      this_id = survey.create_survey("COMP1521","17s2",["1","2","3"],"2017-09-23 00:00:00","2017-09-23 23:59:59")
      print(survey.get_survey("COMP1521","17s2"))
      survey.delete_survey(this_id)
      print(survey.get_survey("COMP1521","17s2"))

    # print(course.get_course())
