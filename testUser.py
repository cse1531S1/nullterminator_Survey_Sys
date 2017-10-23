from user import *
import unittest

class TestAddStudent(unittest.TestCase):

    def setUp(self):
        self.user = UserData()

    def test_add_student_invalid_id(self):
        student_id = ""
        num_student = len(self.user.find("role","student").all())
        with self.assertRaises(TypeError):
            self.user.new_user(student_id)
        curr_num_student = len(self.user.find("role","student").all())
        self.assertEqual(num_student, curr_num_student)

    def test_add_student_valid_id(self):
        student_id = 1220
        student_pass = "student1220"
        student_role = "student"
        self.assertEqual(self.user.findById(student_id), None)
        num_student = len(self.user.find("role","student").all())
        self.user.new_user(student_id,student_pass,student_role)
        curr_num_student = len(self.user.find("role","student").all())
        self.assertEqual(num_student + 1, curr_num_student)
        self.assertNotEqual(self.user.findById(student_id), [])
