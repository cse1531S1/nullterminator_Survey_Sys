from enrolment import *
from survey import * 
import unittest


class TestEnrolment(unittest.TestCase):

    def setUp(self):

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
