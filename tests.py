import unittest
import os

""" All the test cases is written in here. """

from testQuestion import *
from testSurvey import *
from testEnrolment import *
from testUser import *

if __name__ == '__main__':
    # setup a database to this unittest
    os.system("sh init_db.sh")
    # run all the unittest
    unittest.main()

    # clean up the database
    os.system("sh init_db.sh")
