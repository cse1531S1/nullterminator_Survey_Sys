import unittest
from testSurvey import *
from testQuestion import *
from testUser import *


if __name__ == '__main__':
    # startup a database to unittest
    os.system("sh init_db.sh")
    unittest.main()
    # reset the database that use in unittest
    # os.system("sh init_db.sh")
