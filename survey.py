from sql_uti import SqlUtil
from server import app
from enrolment import enrol_Data
from user import UserData

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
        self.__enrol = enrol_Data()
        self.__user = UserData()
        # set up the join search columns
        self.clear()

    def clear(self,join = False, col = False):
        super().clear(join = True, col= True)
        if not col and not join:
            # set up the default join searching order
            self.with_table("course","course_id","id")\
                .col_name("id").col_name(["course_code","course_year"],"course")\
                .col_name(["Q_id","start_time","end_time","status"])
        return self

    def create_survey(self,course_code,course_year,Q_id,start_time,end_time):
        # getthing this course's id
        this_course = self.__course.get_course(course_code,course_year)
        print(this_course)
        self.insert("course_id",this_course[0])\
                        .insert("Q_id","&&".join(Q_id))\
                        .insert("start_time",start_time)\
                        .insert("end_time",end_time).save()
        this_survey = self.find(["course_id","Q_id","start_time","end_time"],\
                        [this_course[0],"&&".join(Q_id),start_time,end_time])\
                        .sort_by("survey.id",False).one()
        return this_survey[0]
    def get_survey(self,course_name= None,course_year = None):
        if not course_name and not course_year:
            # return all the ongoning survey
            return self.all()

        # provided course info
        this_course = self.__course.get_course(course_name, course_year)
        # search all the survey provided by this course
        # join search and select all all the information
        # order by id, course_code, course_year, qid, start_time,end_time,status
        this_sur = self.find(["survey.course_id"],[this_course[0]]).test_exe().all()
        return this_sur

    def get_survey_by_user(self, user_id):
        this_courses =self.__enrol.findById(user_id)
        # getting the class of the user
        this_user = self.__user.findById(user_id)

        print(this_courses)

        if not this_courses:
            # thie user dont enrolled to any courses
            return []
        survey_list =[]
        for course in this_courses:
            # status filter
            if this_user[2] == "staff":
                # only can reach the status echo to 1
                self.findIn("status", ["1","3"], sign = "=")
            elif this_user[2]== "student":
                # only can reach the status echo to 2 and 3
                self.findIn("status", ["2","3"], sign = "=")
            # get the ongoning survey by course
            this_sur =self.get_survey(course[1],course[2])
            if this_sur:
                # if it has survey, apppend in survey_list
                survey_list += this_sur
        # for l in survey_list:
        #     print(l)
        return survey_list

    def is_premitted(self, survey_id, user_id):
        this_sur = self.id_filter(survey_id).test_exe().one()
        his_enrol = self.__enrol.find(["user_id","course_code","course_year"]\
                        ,[user_id,this_sur[1],this_sur[2]]).one()
        if his_enrol:
            return True
        return False


    # status : 0 = just created, 1 = ask for review
    # status : 2 = student access, close = student can access the data
    def __change_status(self,sid, status):
        # post survey to related staff, stage = review
        self.id_filter(sid).update("status",status).save()
        return self

    def post(self,sid):
        # set the status to 1
        return self.__change_status(sid, 1)


    def review(self, sid):
        # post survey to related student, stage = review
        return self.__change_status(sid, 2)

    def close(self, sid):
        # post survey to finished, stage = closed
        return self.__change_status(sid, 3)


    def delete_survey(self,sid):
        if type(sid)!= int:
            raise TypeError("input id must be int")
        self.id_filter(sid).delete()

    def id_filter(self, sid):
        return self.find("survey.id",sid)

    def get_qids(self, sid):
        # getting back an array of question id
        return self.id_filter(sid).one()[3].split("&&")


if __name__ == '__main__':
    course = Course()
    print(course.get_course("COMP1521","17s2"))
    survey = Survey()
    this_id = survey.create_survey("COMP1521","17s2",["1","2","3"],"2017-09-23 00:00:00","2017-09-23 23:59:59")
    print(survey.get_survey("COMP1521","17s2"))
    survey.test_exe().delete_survey(this_id)
    print(survey.get_survey("COMP1521","17s2"))

    # print(course.get_course())
