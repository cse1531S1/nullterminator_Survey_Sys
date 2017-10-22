import unittest
from survey import *
import os


class SurveyTest(unittest.TestCase):
    def setUp(self):
        self.survey = Survey()

    def test_add_no_course_to_survey(self):
        """
        :post : No new additions will appear in the db table
                course_code and course_year should be a non_empty string
        """

        prev_num_survey = len(self.survey.get_survey())
        with self.assertRaises(TypeError):
            self.survey.create_survey(["1","2","3"],"2017-09-23 00:00:00","2017-09-23 23:59:59")

        cur_num_survey = len(self.survey.get_survey())
        self.assertEqual(prev_num_survey, cur_num_survey)

    def test_add_no_question_to_survey(self):
        """
        :post : No new additions will appear in the db table
                qid should be a list that contains all questionid
        """

        prev_num_survey = len(self.survey.get_survey())
        with self.assertRaises(TypeError):
            self.survey.create_survey("COMP1521","17s2","2017-09-23 00:00:00","2017-09-23 23:59:59")

        cur_num_survey = len(self.survey.get_survey())
        self.assertEqual(prev_num_survey, cur_num_survey)

    def test_add_no_time_to_survey(self):
        """
        :post : No new additions will appear in the db table
                start_time and end_time should be a non_empty string
        """

        prev_num_survey = len(self.survey.get_survey())
        with self.assertRaises(TypeError):
            self.survey.create_survey("COMP1521","17s2",["1","2","3"])

        cur_num_survey = len(self.survey.get_survey())
        self.assertEqual(prev_num_survey, cur_num_survey)

    def test_survey_post(self):
        # try to review and post the survey
        self.survey.post(1)
        self.survey.review(1)
    def test_survey_close(self):
        # try to close a running survey
        self.survey.close(1)
