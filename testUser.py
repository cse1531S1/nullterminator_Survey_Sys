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
    def test_register_and_delete(self):
        # register for guest
        self.user.register(2000, "tecty")
        self.user.register(2001, "tecty")
        # both user should be found in database
        assert(self.user.findById(2000))
        assert(self.user.findById(2001))


        # delete a user that has registered
        self.user.deleteById(2001)
        # the user shouldn't be found
        assert(not self.user.findById(2001))

    def test_show_unguest(self):
        # filter for all the not premitted user
        # one has been deleted
        assert(len(self.user.show_unguest()) == 1)
    def test__check_pass(self):
        # simulate login
        assert(self.user.check_pass(2,"tecty"))
        # login fail
        assert(not self.user.check_pass(2,"tecee"))

    def test_find_user(self):
        # default admin user
        assert(self.user.findById(2))
