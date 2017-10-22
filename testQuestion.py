import unittest
from question import Question

class QuestionTest(unittest.TestCase):
    """docstring for QuestionTest."""
    def setUp(self):
        self.question = Question()

    def test_add_question(self):
        """add question to databse"""
        first_id=self.question.add_q("sample question?", "0", "MCQ",["a1","a2"])
        second_id=self.question.add_q( "sample question?", "1", "MCQ",["a1","a2"])
        third_id=self.question.add_q( "sample question?", "0", "TEXT")
        # check whether these are distinct question id
        assert(first_id != second_id)
        assert(first_id != third_id)
        assert(second_id != third_id)
    def test_delete_question(self):
        # try to delete a quesiton in database
        self.question.del_q(1)
        # check whether the question is successfully deleted
        assert(len(self.question.find_q(pool_id = "0"))==1)
        assert(self.question.find_q(q_id=[1]))

    def test_find_all_mandatory(self):
        # check whether the system has exactly 1 question
        # one has deleted
        assert(len(self.question.find_q(pool_id="0"))==1)

    def test_find_all_option(self):
        # check whether the system has exactly 1 question
        assert(len(self.question.find_q(pool_id="1"))==1)
