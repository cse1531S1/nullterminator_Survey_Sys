from question import *
import unittest

class TestQuestion(unittest.TestCase):

    def setUp(self):
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
