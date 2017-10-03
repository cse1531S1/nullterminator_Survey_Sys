from sql_uti import SqlUtil

class enrol_Data(SqlUtil):
    """docstring for enrolment."""
    def __init__(self):
        super().__init__("enrolments")

    def findById(self, uid):
        if not type(uid) in [int,str]:
            raise TypeError("ID for a user muset be a interger")
        # simple case of mapping a function to dynamic execute SQL
        return self.find("user_id",int(uid)).all()

if __name__ == '__main__':
   enrol = enrol_Data()
   print(enrol.findById(125))

