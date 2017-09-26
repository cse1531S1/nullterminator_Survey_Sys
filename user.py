from sql_uti import SqlUtil
from server import app

class User(SqlUtil):
    """docstring for user."""
    def __init__(self):
        super().__init__("users")

    def findById(self, uid):
        if not type(uid) in [int,str]:
            raise TypeError("ID for a user muset be a interger")
        # simple case of mapping a function to dynamic execute SQL
        return self.find("id",int(uid)).one()
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



if __name__ == '__main__':
    with app.app_context():
        user = User()
        # use.print_table()
        print(user.findById(50))

        user.new_user(1,"pass","admin")
        print(user.findById(1))

        print("\nTry to login with the user that I just insert")
        print(user.check_pass(1,"pass"))


        # cleanup the added user
        user.deleteById(1)
        print(user.findById(1))
