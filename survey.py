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
        this_sur = self.find(["survey.course_id"],[this_course[0]]).all()
        return this_sur


    # for update the information of a survey
    def update_survey(self, survey_id, Q_id, start_time = None, end_time = None):
        # get the survey by id
        self.id_filter(survey_id)

        # generate a new list of question id, and update that
        self.update("Q_id","&&".join(Q_id))

        # if it has satrt time, and end_time update that
        if start_time:
            self.update("start_time", start_time)
        if end_time:
            self.update("end_time", end_time)

        # push the changes to database
        return self.save()

    def get_survey_by_user(self, user_id):
        this_courses =self.__enrol.clear(True,True).findById(user_id)
        # getting the class of the user
        this_user = self.__user.findById(user_id)

        print(this_courses)

        if not this_courses:
            # thie user dont enrolled to any courses
            return []
        survey_list =[]

        # id to filte the survey_list
        filter_arr =[]
        # status filter
        if this_user[2] == "staff":
            # only can reach the status echo to 1
            self.findIn("status", ["1","2","3"], sign = "=")
        elif this_user[2]== "student":
            # only can reach the status echo to 2 and 3
            self.findIn("status", ["2","3"], sign = "=")

            # find the which survey this user has submitted

            filter_arr =SqlUtil("respond").find("user_id",this_user[0]).all()
            # get filter_arr only has id of submitted survey
            filter_arr = [this[1] for this in filter_arr]

        # get the ongoning survey by course
        survey_list =self.findIn("course_id", [this[1] for this in this_courses]).all()



        return survey_list

    def is_premitted(self, survey_id, user_id):
        this_sur = self.id_filter(survey_id).one()
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
        return self

    def id_filter(self, sid):
        return self.find("survey.id",sid)

    def get_qids(self, sid):
        # getting back an array of question id
        qids = self.id_filter(sid).one()[3]
        if qids:
            # prevent the error caused by qids is empty string
            qids = qids.split("&&")
            qids = [int(this_id) for this_id in qids]
        else:
            qids  =[]
        return qids

if __name__ == '__main__':
    course = Course()
    print(course.get_course("COMP1521","17s2"))
    survey = Survey()
    this_id = survey.create_survey("COMP1521","17s2",["1","2","3"],"2017-09-23 00:00:00","2017-09-23 23:59:59")
    print(survey.get_survey("COMP1521","17s2"))
    survey.test_exe().delete_survey(this_id)
    print(survey.get_survey("COMP1521","17s2"))

    # print(course.get_course())
