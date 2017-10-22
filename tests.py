import unittest
import os
import sqlite3
from question import *
from survey import *
from sql_uti import *
from enrolment import *

# class TestPoolQuestion(unittest.TestCase):
#
#     def setUp(self):
#         os.system("db/init_db.sh")
#         self.question = Question()
#
#     def tearDown(self):
#         os.remove("db/survey.db")


# class TestSurvey(unittest.TestCase):
#
#     def setUp(self):
#         os.system("db/init_db.sh")
#         self.survey = Survey()
#
#     def test_insert_empty_questions(self):
#         with self.assertRaises(TypeError):
#             self.survey.create_survey('0')
#
#     def tearDown(self):
#         os.remove("db/survey.db")

# class TestEnrolStudent(unittest.TestCase):
#
#     def setUp(self):
#         os.system("db/init_db.sh")
#         self.enrol = SqlUtil("users")
#
#     def test_add_student_invalid_id(self):
#         student_id = ""
#         num_student = len(self.enrol.find("role","student").all())
#         with self.assertRaises(TypeError):
#             self.enrol.insert(["id"],student_id).save()
#         curr_num_student = len(self.enrol.find("role","student").all())
#         self.assertEqual(num_student, curr_num_student)
#
#     def test_add_student_valid_id(self):
#         student_id = 1220
#         student_pass = "student1220"
#         student_role = "student"
#         self.assertEqual(self.enrol.find("id",student_id).all(), [])
#         num_student = len(self.enrol.find("role","student").all())
#         self.enrol.insert(["id","password","role"],[student_id,student_pass,student_role]).save()
#         curr_num_student = len(self.enrol.find("role","student").all())
#         self.assertEqual(num_student + 1, curr_num_student)
#         self.assertNotEqual(self.enrol.find("id",student_id).all(), [])
#
#     def tearDown(self):
#         os.remove("db/survey.db")

# class TestEnrolment(unittest.TestCase):
# 
#     def setUp(self):
#         os.system("db/init_db.sh")
#         self.enrol = SqlUtil("enrolments")
#         self.user = SqlUtil("users")
#         self.course = SqlUtil("course")


if __name__ == '__main__':
    unittest.main()
