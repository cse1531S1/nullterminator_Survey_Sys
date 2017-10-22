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
        :post : No new additions will appear in the survey.db table
                course_code and course_year should not be empty
                
        """
        prev_num_survey = len(self.survey.get_survey(None,None))
        with self.assertRaises(TypeError):
            self.survey.create_survey(["1","2","3"],"2017-09-23 00:00:00","2017-09-23 23:59:59")

        cur_num_survey = len(self.survey.get_survey(None,None))
        self.assertEqual(prev_num_survey, cur_num_survey)

    def test_add_invaild_course_to_survey(self):
        """
        :post : No new additions  will appear in the survey.db table
                course_code and course_year should be match
                
        """
        course_code = "abc"
        course_year = "123"
        prev_num_survey = len(self.survey.get_survey(None,None))
        with self.assertRaises(TypeError):
            self.survey.create_survey(course_code,course_year,["1","2","3"],"2017-09-23 00:00:00","2017-09-23 23:59:59")
        cur_num_survey = len(self.survey.get_survey(None,None))
        self.assertEqual(prev_num_survey, cur_num_survey)
        
    def test_add_no_question_to_survey(self):
        """
        :post : No new additions will appear in the survey.db table
                qid should not be empty
        """
     
        prev_num_survey = len(self.survey.get_survey(None,None))
        with self.assertRaises(TypeError):
            self.survey.create_survey("COMP1521","17s2","2017-09-23 00:00:00","2017-09-23 23:59:59")

        cur_num_survey = len(self.survey.get_survey(None,None))
        self.assertEqual(prev_num_survey, cur_num_survey)
    
    def test_add_invaild_question_to_survey(self):
        """
        :post : No new additions will appear in the db table
                qid should be a list of only numbers that contains all questionid
        """
        qid = "questionid"
        prev_num_survey = len(self.survey.get_survey(None,None))
        #with self.assertRaises(TypeError):
        self.survey.create_survey("COMP1521","17s2",qid,"2017-09-23 00:00:00","2017-09-23 23:59:59")

        cur_num_survey = len(self.survey.get_survey(None,None))
        self.assertEqual(prev_num_survey, cur_num_survey)
        
    def test_add_no_time_to_survey(self):
        """
        :post : No new additions will appear in the survey.db table
                start_time and end_time should not be empty
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



    def tearDown(self):
        os.remove("db/survey.db")
    

    
if __name__ == '__main__':
    unittest.main()
    
