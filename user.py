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
        if not this_user:
            raise TypeError("Currently the database has not this user.")

        if password == this_user[1]:
            # check it's password and they are same
            return True
        else:
            return False

    def new_user(self,uid, password,role):
        if not (uid and password and role):
            raise TypeError("The user_name, user_id, password must be all setted")
        if not role in ["staff","student","admin","unguest"]:
            raise TypeError("Undefined role for this user.")
        try:
            # store the information in the class
            self.insert(["id","password","role"],[uid,password,role]).save()
        except Exception as e:
            # The database couldn't isert
            raise TypeError('This id Has been used.Please use another user id.')
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
        # try to insert into database, by a defined function
        self.new_user(uid, pw, 'unguest')

        return True
    def show_unguest(self):
        # return a list of all the unauthorised guest
        return self.find("role","unguest").all()


class EnrolRequest(SqlUtil):
    """Table for all the enrol request form guest."""
    def __init__(self):
        super().__init__("enrol_request")

    def id_filter(self, require_id):
        return self.find("id",require_id)
    def get_requests(self):
        # return all the enrol request of guest
        # bulid the sql by join table search
        self.with_table("course", "course_id", "id")
        self.col_name(["id","user_id"])
        self.col_name(["course_code","course_year"],"course")
        request_l = self.all()
        # clean the join search config
        self.clear(True,True)
        # return the current request
        return request_l

    def premit_request(self, require_id):
        # try to find according enrol request
        request = self.id_filter(require_id).one()
        if not request:
            # couln't handle this premit
            raise TypeError("The enrol request is not exist")
        # enrol that course for that user
        enrol_Data().enrol(request[1], request[2])
        # delete the record for require
        self.id_filter(require_id).delete()
        # if not andy error, would return True
        return True
    def deny_request(self, require_id):
        # try to find according enrol request
        request = self.id_filter(require_id).one()
        if not request:
            # couln't handle this premit
            raise TypeError("The enrol request is not exist")
        return self.id_filter(require_id).delete()

    def enrol_user(self, uid, course_id):
        if enrol_Data().find(["user_id","course_id"],[uid,course_id]).all():
            raise TypeError("This course has been enrolled by yourself.")
        if self.find(["user_id","course_id"],[uid,course_id]).all():
            raise TypeError("This course have been requested by yourself.")
        # Success insert this request
        self.insert(["user_id","course_id"], [uid,course_id]).save()
    def deny_user(self, uid):
        # delete all the request by a user
        return self.find("user_id",uid).delete()


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
        if self.__pw == pw:
            # if this user is not premit by admin, he couldn't login
            if self.role == "unguest":
                raise TypeError("Please wait for admin to approve your register.")
            # is premited by admin
            return True
        raise TypeError("Wrong username/password, please try again.")
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
        UserData().id_filter(uid).update("role","guest").save()
    def deny_register(self, uid):
        # delete the user in the database
        UserData().id_filter(uid).delete()
        # delete the enrol request in the database
        EnrolRequest().deny_user(uid)
    def premit_enrol(self, require_id):
        # call the function in EnrolRequest to do the enrolments
        EnrolRequest().premit_request(require_id)
    def deny_enrol(self, require_id):
        # call the function in EnrolRequest to do this
        EnrolRequest().deny_request(require_id)


class Student(User):
    """docstring for Student."""
    def is_student(self):
        return True

class Guest(User):
    """docstring for Guest."""
    def is_authenticated(self):

        return True
    def is_guest(self):
        return True
    def enrol(self,course_id):
        EnrolRequest().enrol_user(self.uid, course_id)

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
