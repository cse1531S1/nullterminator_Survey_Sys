import unittest
from survey import *
import os
import sqlite3


class SurveyTest(unittest.TestCase):
    def setUp(self):
        os.system("sh init_db.sh")
        self.survey = Survey()  
     
        
    def test_add_no_course_to_survey(self):
        """
        :post : No new additions will appear in the db table
                course_code and course_year should be a non_empty string
                
        """
        prev_num_survey = len(self.survey.get_survey(None,None))
        with self.assertRaises(TypeError):
            self.survey.create_survey(["1","2","3"],"2017-09-23 00:00:00","2017-09-23 23:59:59")

        cur_num_survey = len(self.survey.get_survey(None,None))
        self.assertEqual(prev_num_survey, cur_num_survey)
        
    def test_add_no_question_to_survey(self):
        """
        :post : No new additions will appear in the db table
                qid should be a list that contains all questionid
        """
     
        prev_num_survey = len(self.survey.get_survey(None,None))
        with self.assertRaises(TypeError):
            self.survey.create_survey("COMP1521","17s2","2017-09-23 00:00:00","2017-09-23 23:59:59")

        cur_num_survey = len(self.survey.get_survey(None,None))
        self.assertEqual(prev_num_survey, cur_num_survey)
        
    def test_add_no_time_to_survey(self):
        """
        :post : No new additions will appear in the db table
                start_time and end_time should be a non_empty string
        """
      
        prev_num_survey = len(self.survey.get_survey(None,None))
        with self.assertRaises(TypeError):
            self.survey.create_survey("COMP1521","17s2",["1","2","3"])

        cur_num_survey = len(self.survey.get_survey(None,None))
        self.assertEqual(prev_num_survey, cur_num_survey)
        
    def test_successfully_add_survey_to_db(self):
        """
        :post : new additions will appear in the db table
        """
        prev_num_survey = len(self.survey.get_survey(None,None))
        self.sid = self.survey.create_survey("COMP1521","17s2",["1","2","3"],"2017-09-23 00:00:00","2017-09-23 23:59:59")
        cur_num_survey = len(self.survey.get_survey(None,None))
        self.assertEqual(prev_num_survey+1, cur_num_survey)
        s = self.survey.get_survey("COMP1521","17s2")
        self.assertEqual(s[3], "1&&2&&3")
        self.assertEqual(s[4], "2017-09-23 00:00:00")
        self.assertEqual(s[5], "2017-09-23 23:59:59")

    def test_successfully_post_survey_to_staff(self):
        """
        :post : survey_status will change from 0 to 1
                status is represented as a char
        """
        s = self.survey.get_survey("COMP1521","17s2")
        status = s[-1]
        self.assertEqual(status, 0)
        sid = s[0]
        self.survey.post(sid)
        s = self.survey.get_survey("COMP1521","17s2")
        status = s[-1]
        self.assertEqual(status, 1)


    def test_successfully_post_survey_to_student(self):
        """
        :post : survey_status will change from 1 to 2
                status is represented as a char
        """
        s = self.survey.get_survey("COMP1521","17s2")
        status = s[-1]
        self.assertEqual(status, 1)
        sid = s[0]
        self.survey.review(sid)
        s = self.survey.get_survey("COMP1521","17s2")
        status = s[-1]
        self.assertEqual(status, 2)

    def test_successfully_close_survey(self):
        """
        :post : survey_status will change from 2 to 3
                status is represented as a char
        """
        s = self.survey.get_survey("COMP1521","17s2")
        status = s[-1]
        self.assertEqual(status, 2)
        sid = s[0]
        self.survey.close(sid)
        s = self.survey.get_survey("COMP1521","17s2")
        status = s[-1]
        self.assertEqual(status, 3)

    def tearDown(self):
        os.remove("db/survey.db")
    

    
if __name__ == '__main__':
    unittest.main()
    
