from user import *
import unittest


class TestUserData(unittest.TestCase):
    """TestCase for table handling of user data."""
    def setUp(self):
        # handy quote for user data class
        self.usr = UserData()
    def test_register_and_delete(self):
        # register for guest
        self.usr.register(2000, "tecty")
        self.usr.register(2001, "tecty")
        # both user should be found in database
        assert(self.usr.findById(2000))
        assert(self.usr.findById(2001))


        # delete a user that has registered
        self.usr.deleteById(2001)
        # the user shouldn't be found
        assert(not self.usr.findById(2001))

    def test_show_unguest(self):
        # filter for all the not premitted user
        # one has been deleted
        assert(len(self.usr.show_unguest()) == 1)
    def test__check_pass(self):
        # simulate login
        assert(self.usr.check_pass(2,"tecty"))
        # login fail
        assert(not self.usr.check_pass(2,"tecee"))

    def test_find_usr(self):
        # default admin user
        assert(self.usr.findById(2))
