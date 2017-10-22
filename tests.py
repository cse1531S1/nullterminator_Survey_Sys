import unittest
import os
import sqlite3
from question import *
from survey import *
from sql_uti import *
from enrolment import *

class TestPoolQuestion(unittest.TestCase):

    def setUp(self):
        os.system("db/init_db.sh")
        self.question = Question()

    def test_add_mandatory_MCQ_valid(self):
        q = "What is your name?"
        # pool id for mandatory is 0
        pool = "0"
        # question type is either MCQ or TEXT
        q_type = "MCQ"
        # MCQ answer in the form of list
        answer = ["Tom","Dick","Harry"]

        num_questions = len(self.question.find_q(pool_id = "0"))
        self.question.add_q(q,pool,q_type,answer)
        curr_num_questions = len(self.question.find_q(pool_id = "0"))
        self.assertEqual(num_questions + 1,curr_num_questions)

    def test_add_optional_TEXT_valid(self):
        q = "What is your name?"
        # pool id for optional is 1
        pool = "1"
        # question type is either MCQ or TEXT
        q_type = "TEXT"

        num_questions = len(self.question.find_q(pool_id = "1"))
        self.question.add_q(q,pool,q_type)
        curr_num_questions = len(self.question.find_q(pool_id = "1"))
        self.assertEqual(num_questions + 1,curr_num_questions)

    def test_delete_inserted_question_valid(self):
        q = "How is your day?"
        #pool id for mandatory is 0
        pool = "0"
        # question type is either MCQ or TEXT
        q_type = "TEXT"

        num_questions = len(self.question.find_q(pool_id = "0"))
        # inserting question will return an ID
        this_question_id = self.question.add_q(q,pool,q_type)
        # delete inserted question above
        self.question.del_q(this_question_id)
        curr_num_questions = len(self.question.find_q(pool_id = "0"))
        self.assertEqual(num_questions,curr_num_questions)

    def tearDown(self):
        os.remove("db/survey.db")


class TestSurvey(unittest.TestCase):

    def setUp(self):
        os.system("db/init_db.sh")
        self.survey = Survey()

    def test_add_no_course_to_survey(self):
        """
        :post : No new additions will appear in the survey.db table
                course_code and course_year should not be empty
        """
        prev_num_survey = len(self.survey.get_survey())
        with self.assertRaises(TypeError):
            self.survey.create_survey(["1","2","3"],"2017-09-23 00:00:00","2017-09-23 23:59:59")
        cur_num_survey = len(self.survey.get_survey())
        self.assertEqual(prev_num_survey, cur_num_survey)

    def test_add_invalid_course_to_survey(self):
        """
        :post : No new additions  will appear in the survey.db table
                course_code and course_year should be match
        """
        course_code = "abc"
        course_year = "123"
        prev_num_survey = len(self.survey.get_survey())
        with self.assertRaises(TypeError):
            self.survey.create_survey(course_code,course_year,["1","2","3"],"2017-09-23 00:00:00","2017-09-23 23:59:59")
        cur_num_survey = len(self.survey.get_survey())
        self.assertEqual(prev_num_survey, cur_num_survey)

    def test_add_no_question_to_survey(self):
        """
        :post : No new additions will appear in the survey.db table
                qid should not be empty
        """
        prev_num_survey = len(self.survey.get_survey())
        with self.assertRaises(TypeError):
            self.survey.create_survey("COMP1521","17s2","2017-09-23 00:00:00","2017-09-23 23:59:59")
        cur_num_survey = len(self.survey.get_survey())
        self.assertEqual(prev_num_survey, cur_num_survey)

    def test_add_no_time_to_survey(self):
        """
        :post : No new additions will appear in the survey.db table
                start_time and end_time should not be empty
        """
        prev_num_survey = len(self.survey.get_survey())
        with self.assertRaises(TypeError):
            self.survey.create_survey("COMP1521","17s2",["1","2","3"])
        cur_num_survey = len(self.survey.get_survey())
        self.assertEqual(prev_num_survey, cur_num_survey)

    def test_successfully_add_survey_to_db(self):
        """
        :post : new additions will appear in the db table
        """
        prev_num_survey = len(self.survey.get_survey())
        self.sid = self.survey.create_survey("COMP1521","17s2",["1","2","3"],"2017-09-23 00:00:00","2017-09-23 23:59:59")
        cur_num_survey = len(self.survey.get_survey())
        self.assertEqual(prev_num_survey + 1, cur_num_survey)
        s = self.survey.get_survey("COMP1521","17s2")
        self.assertEqual(s[3], "1&&2&&3")
        self.assertEqual(s[4], "2017-09-23 00:00:00")
        self.assertEqual(s[5], "2017-09-23 23:59:59")

    def tearDown(self):
        os.remove("db/survey.db")

class TestEnrolment(unittest.TestCase):

    def setUp(self):
        os.system("db/init_db.sh")
        self.enrol = enrol_Data()
        self.course = Course()

    def test_enrol_valid(self):
        zID = 571
        course_code = "COMP1531"
        course_year = "17s2"
        course_id = self.course.get_course(course_code, course_year)[0]
        enrol_list = self.enrol.findById(zID)
        assert [zID, course_code, course_year] not in enrol_list
        prev_student_courses = len(enrol_list)
        self.enrol.insert(["user_id","course_id"],[zID,course_id]).save()
        curr_enrol_list = self.enrol.findById(zID)
        curr_student_courses = len(curr_enrol_list)
        self.assertEqual(prev_student_courses + 1, curr_student_courses)

    def tearDown(self):
        os.remove("db/survey.db")

class TestAddStudent(unittest.TestCase):

    def setUp(self):
        os.system("db/init_db.sh")
        self.user = SqlUtil("users")

    def test_add_student_invalid_id(self):
        student_id = ""
        num_student = len(self.user.find("role","student").all())
        with self.assertRaises(TypeError):
            self.user.insert(["id"],student_id).save()
        curr_num_student = len(self.user.find("role","student").all())
        self.assertEqual(num_student, curr_num_student)

    def test_add_student_valid_id(self):
        student_id = 1220
        student_pass = "student1220"
        student_role = "student"
        # assert if student have not been inserted by comparing
        # with empty list
        self.assertEqual(self.user.find("id",student_id).all(), [])
        num_student = len(self.user.find("role","student").all())
        self.user.insert(["id","password","role"],[student_id,student_pass,student_role]).save()
        curr_num_student = len(self.user.find("role","student").all())
        self.assertEqual(num_student + 1, curr_num_student)
        self.assertNotEqual(self.user.find("id",student_id).all(), [])

    def tearDown(self):
        os.remove("db/survey.db")

if __name__ == '__main__':
    unittest.main()
