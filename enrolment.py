from sql_uti import SqlUtil

class enrol_Data(SqlUtil):
    """docstring for enrolment."""
    def __init__(self):
        super().__init__("enrolments")
        self.clear()
    def clear(self, join = False, col = False):
        # overwrite the father function to set up default in __from
        super().clear(True,True)
        if not col and not join:
            # reset the col value and join serach
            self.with_table("course","course_id","id")

            # in default only three column would show
            self.col_name("user_id")
            # show the column in the course table
            self.col_name(["course_code","course_year"], table_name ="course")

    def findById(self, uid):
        if not type(uid) in [int,str]:
            raise TypeError("ID for a user muset be a interger")
        # simple case of mapping a function to dynamic execute SQL
        return self.find("user_id",int(uid)).all()


if __name__ == '__main__':
   enrol = enrol_Data()
   print(enrol.findById(125))
