from db.sql_uti import SqlUtil

class Course(SqlUtil):
    """docstring for Course."""
    def __init__(self):
        super().__init__("course")
    def get_course_id(self,course_code,course_year):
        this_course = self.find("course_code",course_code)\
                        .find("course_year",course_year).one()
        return int(this_course[0])

class Survey(SqlUtil):
    """docstring for survey."""
    def __init__(self):
        super().__init__("survey")
        self.__course = Course()
    def create_survey(self,course_code,course_year,q_id,start_time,end_time):
        this_course_id = self.__course.get_course_id(course_code,course_year)
        self.insert("course_id",this_course_id).insert("q_id","&&".join(q_id))\
                        .insert("start_time",start_time)\
                        .insert("end_time",end_time).save()
        this_survey = self.find(["course_id","q_id","start_time","end_time"],\
                        [this_course_id,"&&".join(q_id),start_time,end_time])\
                        .sort_by("id",False).one()
        return this_survey[0]
    def get_survey(self,course_code,course_year):
        this_course_id = self.__course.get_course_id(course_code,course_year)
        return self.find("course_id",this_course_id).all()
    def delete_survey(self,id):
        if type(id)!= int:
            raise TypeError("input id must be int")
        self.find("id",id).delete()

if __name__ == '__main__':
    course  = Course()
    print(course.get_course_id("COMP1521","17s2"))
    survey = Survey()
    this_id = survey.create_survey("COMP1521","17s2",["1","2","3"],"2017-09-23 00:00:00","2017-09-23 23:59:59")
    print(survey.get_survey("COMP1521","17s2"))
    survey.delete_survey(this_id)
    print(survey.get_survey("COMP1521","17s2"))
