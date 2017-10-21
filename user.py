from sql_uti import SqlUtil
from flask_login import UserMixin
from enrolment import enrol_Data


class UserData(SqlUtil):
    """docstring for user."""
    def __init__(self):
        super().__init__("users")

    def findById(self, uid):
        # simple case of mapping a function to dynamic execute SQL
        return self.id_filter(uid).one()
    def check_pass(self,uid,password):
        # get the users information by self function
        this_user = self.findById(uid)
        if password == this_user[1]:
            # check it's password and they are same
            return True
        else:
            return False

    def new_user(self,uid, password,role):
        if not (uid and password and role):
            raise TypeError("The user_name, user_id, password must be all setted")
        if not role in ["staff","student","admin"]:
            raise TypeError("Undefined role for this user.")

        # store the information in the class
        self.insert(["id","password","role"],[uid,password,role]).save()
        # return self to have the property of one online execution
        return self
    def deleteById(self, uid):
        if not type(uid) in [int,str]:
            raise TypeError("User id must be int or string")
        self.find("id",int(uid)).delete()
    def id_filter(self, uid):
        if not type(uid) in [int,str]:
            # not provide valid userid
            raise TypeError("ID for a user muset be a interger")
        # passed the filtered user
        return self.find("id",int(uid))
    def register(self, uid, pw):
        if not uid or not pw:
            raise TypeError("Please provide password or user id.")
        if int(uid) < 0:
            raise TypeError("User id must be greater than 0.")
        try:
            # try to insert into database
            self.insert(['id','password','role'],[uid,pw,'unguest']).save()
        except Exception as e:
            # The database couldn't isert
            raise TypeError('This id Has been used.Please use another user id.')
        return True

class EnrolRequest(SqlUtil):
    """Table for all the enrol request form guest."""
    def __init__(self):
        super().__init__("enrol_request")

    def id_filter(self, require_id):
        return self.find("id",require_id)
    def get_requests(self):
        # return all the enrol request of guest
        return self.all()
    def premit_request(self, require_id):
        # try to find according enrol request
        request = self.id_filter(require_id).one()
        if not request:
            # couln't handle this premit
            raise TypeError("The enrol request is not exist")
        # enrol that course for that user
        enrol_Data().enrol(request[1], request[2])
        return True


class User(UserMixin):
    """docstring for User."""
    def __init__(self, user_id):
        super(User, self).__init__()
        self.__usr = UserData()
        this_user = self.__usr.findById(user_id)
        if this_user:
            self.uid = this_user[0]
            self.__pw = this_user[1]
            self.role = this_user[2]
        else:
            return None

    def check_pass(self, pw):
        return self.__pw == pw
    def is_active(self):
        return True
    def get_id(self):
        return self.uid
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False

    def is_admin(self):
        return False
    def is_staff(self):
        return False
    def is_student(self):
        return False
    def is_guest(self):
        return False


class Staff(User):
    def is_staff(self):
        return True

class Admin(User):
    """docstring for Admin."""
    def is_admin(self):
        return True
    def permit_register(self, uid):
        # permit another user to be registered
        self.__usr.id_filter(uid).update("role","guest").save()
    def deny_register(self, uid):
        self.__usr.id_filter(uid).delete()
    def premit_enrol(self, require_id):
        pass
    def deny_enrol(self, require_id):
        pass

class Student(User):
    """docstring for Student."""
    def is_student(self):
        return True

class Guest(User):
    """docstring for Guest."""
    def is_guest(self):
        return True

if __name__ == '__main__':

    user = UserData()
    # use.print_table()
    print(user.findById(50))

    user.test_exe().new_user(1,"pass","admin")
    print(user.findById(1))

    print("\nTry to login with the user that I just insert")
    print(user.check_pass(1,"pass"))


    # cleanup the added user
    user.deleteById(1)
    print(user.findById(1))
