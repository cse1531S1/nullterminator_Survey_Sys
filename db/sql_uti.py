import sqlite3
import csv

# config of the database name
__dbName = "survey.db"

# db connection
conn = sqlite3.connect(__dbName)

class val_pair(object):
    """docstring for val_pair ."""
    def __init__(self):
        super(val_pair, self).__init__()
        self.__key = []
        self.__value = []
    def push(self, key,value):
        if type(key) == str and (type(value)==int  or type(value)==str ):
            # key is a string to serch
            self.__key.append(key)
            self.__value.append(value)
        elif type(key) == list and type(value)==list and len(value) == len(key):
            # the input are both list, push to record
            self.__key += key
            self.__value += value
        else:
            # couldn't handle this type
            raise TypeError
    def get_key(self):
        return self.__key
    def get_value(self):
        return self.__value
    def clear(self):
        # clear all the value store in this instance
        self.__key = []
        self.__value = []

class sql_util(object):
    """docstring for sql_util."""
    def __init__(self, table_name):
        super(sql_util, self).__init__()
        self.__conn = conn
        self.__table_name = table_name;
        # operation for this query defualt is select
        self.__operator = "SELECT"

        # colomn that would selected by this query
        self.__from = []
        # pair for searching ( where operation)
        self.__key_pair = val_pair()
        # pair for insert or update
        self.__data_pair = val_pair()

        # join search for another table
        self.__join = []
        # specify key for join
        self.__join_key = []

    def __where(self):
        # resolve the where sentense
        if self.__key_pair.get_key() or self.__join_key:
            return " WHERE "+" and ".join(self.__join_key+[ key+"?" for key in self.__key_pair.get_key()])
        # if nothing to search, return nothing
        return ""
    def __sql(self):
        # generate the sql sentense
        sql = self.__operator+" "
        if self.__from:
            # has define some col
            sql += ",".join(self.__from)
            # add a space to split words
            sql +=  " "
        elif self.__operator == "DELETE":
            # do nothing
            pass
        else:
            sql += " * "
        # add the table_name
        sql+= "FROM "+ self.__table_name
        if self.__join:
            # mutiple table search
            sql+= ","+ ",".join(self.__join)


        # try to append the search value
        sql += self.__where()
        # end of the sql sentense
        sql +=";"



        return sql


    def col_name(self, col, table_name = None):
        if not table_name:
            # because default value would use self so use
            # this way to specify the table_name
            table_name = self.__table_name
        if type(col) == str:
            # only have one column to find
            self.__from.append(table_name.col)
        elif type(col) == list:
            # the input is for mutiple search
            self.__form += [table_name+item for item in col]
        else:
            # couldn't handle this type
            raise TypeError
        return self

    def with_table(self, table_name, source_key, dest_key):
        if type(table_name)!=str or type(source_key)!= str or \
            type(dest_key) != str:
            # three input value must be string
            raise TypeError

        self.__join.append(table_name)
        # generate the join key_word connection
        self.__join_key.append(self.__table_name + "."+ source_key+"="+ table_name+"."+dest_key)
        return self

    def find(self, col, key_word, sign = "="):
        # set the this criteria into the variable
        # for where xxx = xxx
        self.__key_pair.push(col+sign, key_word)
        return self

    # insert part (low level function)
    def insert(self, key, values ):
        #  push the thing should be insert into data_pair
        self.__data_pair.push(key, values)
        # set the operator to INSERT INTO
        self.__operator = "INSERT INTO"
        return self
    def update(self, key,values):
        # user want the update operation
        self.insert(key, values)
        self.__operator = "UPDATE"
        return self
    def delete(self):
        #  delete somthing form the database
        self.__operator = "DELETE"
        return_list =self.__conn.execute(self.__sql(),self.__data_pair.get_value()+self.__key_pair.get_value()).fetchone()
        #  clear all the list have been used
        self.clear()
        # push the changes
        self.__conn.commit()
        return self

    def one(self):
        return_list =self.__conn.execute(self.__sql(),self.__data_pair.get_value()+self.__key_pair.get_value()).fetchone()
        #  clear all the list have been used
        self.clear()
        # return the search result
        return return_list

    def all(self):
        # convey the varable setted to a valid sql sentense and query the
        # database, collect the result and resent back the data
        return_list = self.__conn.execute(self.__sql(),self.__data_pair.get_value()+self.__key_pair.get_value()).fetchall()
        #  clear all the list have been used
        self.clear()
        # return the buffer
        return return_list
    def save(self):
        # generate the sql by input things for C,U
        if not self.__operator in ["INSERT INTO","UPDATE"]:
            # save method for force commit
            self.__conn.commit()
            return self
        # it is CU operation
        sql = self.__operator + " "+ self.__table_name + " "
        if self.__operator == "INSERT INTO":
            # generate the column name
            sql += " (" +",".join(self.__data_pair.get_key())+") "
            sql += "VALUES (" +",".join(["?" for item in self.__data_pair.get_value()]) +")"
        elif self.__operator == "UPDATE":
            # add a place holder into the sentence
            sql += " SET "+", ".join([key+"=?"for key in self.__data_pair.get_key()])
            sql += self.__where() +";"

        # execute the data operation
        self.__conn.execute(sql,self.__data_pair.get_value()+ self.__key_pair.get_value())

        # clear all the temp data
        self.clear()

        # save the changes
        self.__conn.commit()
        return self
    def clear(self,join = False):
        # clear the join info
        if join:
            self.__join= []
            self.__join_key =[]

        # reset the values
        self.__from = []
        self.__operator = "SELECT"
        self.__key_pair.clear()
        self.__data_pair.clear()
if __name__ == '__main__':
    __dbName = "../"+ __dbName

    enrol = sql_util("enrolments")
    user = sql_util("users")
    course = sql_util("course")
    print("test find all courses that enroled by user_id = 332")
    user332 = enrol.find("user_id", 332, sign = "=").all()
    print(user332)

    print("\ntest find one course that enroled by user_id = 445")
    user445 = enrol.find("user_id", 445, sign = "=").one()
    print(user445)

    # try the function of join search
    enrol.with_table("users","user_id","user_id")
    # select one info about comp1521
    print("\ntest join search of users and enrolments table")
    course1521 = enrol.find("course_code", "COMP1521").one()
    print (course1521)
    # select one info about 18s1
    year18s1 = enrol.find("course_year", "18s1").one()
    print (year18s1)

    print("\ntest whether the class works with users table")
    user333 =user.find("user_id", 333).one()
    print(user333)
    print("\nTest find all the course_code is 1511 and course_year is 17s2 (mutiple criteria search)")
    course1511 = course.find("course_code", "COMP1511").find("course_year","17s2").all()
    print(course1511)


    # Test for insert update and delete

    print("\nTest whether user 1 have record:")
    print(user.find("user_id",1).all())
    user.insert(["user_id","user_name","password"],[1,"toby","test"]).save()

    print("\nTest whether user 1 have recorded:")
    print(user.find("user_id",1).one())

    print("\nMoidfy the value to name of tecty")
    user.find("user_id",1).update("user_name", "tecty").save()
    print(user.find("user_id",1).one())

    print("\nDelete the inserted item")
    user.find("user_id",1).delete()
    print("\nTest whether user 1 have been deleted:")
    print(user.find("user_id",1).all())

    # # too long to print
    # print("\nTest find all the courses in 17s2")
    # year17s2 = course.find("course_year", "17s2").all()
    # print(year17s2)
