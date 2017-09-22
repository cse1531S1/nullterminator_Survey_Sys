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

class SqlUtil(object):
    """docstring for sql_util."""
    def __init__(self, table_name):
        super(SqlUtil, self).__init__()
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

        # sort column specify
        self.__sort_by = []

        # indicator of whether print the SQL information
        self.__test = False

    def __where(self):
        # resolve the where sentense
        if self.__key_pair.get_key() or self.__join_key:
            return " WHERE "+" and "\
                    .join(self.__join_key+\
                    [ key+"?" for key in self.__key_pair.get_key()])
        # if nothing to search, return nothing
        return ""
    def __sql(self):
        # generate the sql sentense
        sql = self.__operator+" "
        if self.__operator in ["SELECT","DELETE"]:

            if self.__operator == "DELETE":
                # do nothing
                pass
            elif self.__from:
                # has define some col
                sql += ",".join(self.__from)
                # add a space to split words
                sql +=  " "
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
            if self.__operator == "SELECT" and self.__sort_by:
                # sort only can be used by select
                sql += " ORDER BY " + " ,"\
                        .join(self.__sort_by)

        elif self.__operator == "INSERT INTO":
            # directly append the table_name
            sql += self.__table_name + " "

            # generate the column name
            sql += " (" +",".join(self.__data_pair.get_key())+") "
            sql += "VALUES (" +",".join(["?" \
                    for item in self.__data_pair.get_value()]) +")"
        elif self.__operator == "UPDATE":
            # directly append the table_name
            sql += self.__table_name + " "
            # add a place holder into the sentence
            sql += " SET "+", ".join([key+"=?" \
                                    for key in self.__data_pair.get_key()])
            sql += self.__where()

        sql +=";"
        return sql


    def col_name(self, col, table_name = None):
        if not table_name:
            # because default value would use self so use
            # this way to specify the table_name
            table_name = self.__table_name
        if type(col)==str:
            # only have one column to find
            self.__from.append(table_name+"."+col)
        elif type(col) == list:
            # the input is for mutiple search
            self.__from += [table_name+"."+item for item in col]
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
        self.__join_key.append(self.__table_name + "."+ source_key+"="\
                                + table_name+"."+dest_key)
        return self

    def find(self, col, key_word, sign = "="):
        # set the this criteria into the variable
        if type(col)== list and type(key_word) == list\
            and len(col)==len(key_word):
            # Polymorphism support for this class
            self.__key_pair.push([c+sign for c in col], key_word)
        elif type(col)==str:
            # for where xxx = xxx
            self.__key_pair.push(col+sign, key_word)
        else:
            raise TypeError("Code Error: couldn't handle this type of column value.")
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

        # for debug
        self.__print_exe()

        return_list =self.__conn.execute(self.__sql(),\
                                        self.__data_pair.get_value()\
                                        +self.__key_pair.get_value())\
                                        .fetchone()
        #  clear all the list have been used
        self.clear()
        # push the changes
        self.__conn.commit()
        return self

    def one(self):

        # for debug
        self.__print_exe()

        # only fetch one instance from database
        return_list =self.__conn.execute(self.__sql(),\
                        self.__data_pair.get_value()\
                        +self.__key_pair.get_value()).fetchone()
        #  clear all the list have been used
        self.clear()
        # return the search result
        return list(return_list)

    def all(self):
        # convey the varable setted to a valid sql sentense and query the
        # database, collect the result and resent back the data

        # for debug
        self.__print_exe()

        return_list = self.__conn.execute(self.__sql(),\
                        self.__data_pair.get_value()\
                        +self.__key_pair.get_value()).fetchall()
        #  clear all the list have been used
        self.clear()
        # return the buffer
        return [list(item) for item in return_list]
    def sort_by(self, col, ascdending = True):
        # sort by the col name provide, only use in select
        if type(col) == list:
            if ascdending:
                col = [item + " ASC" for item in col ]
            else:
                col = [item + " DESC" for item in col ]
            self.__sort_by += col
        if type(col) == str:
            if ascdending:
                col += " ASC"
            else:
                col += " DESC"
            self.__sort_by.append(col)
        return self
    def save(self):
        # generate the sql by input things for C,U
        if not self.__operator in ["INSERT INTO","UPDATE"]:
            # save method for force commit
            self.__conn.commit()
            return self

        # for debug
        self.__print_exe()

        # execute the data operation
        self.__conn.execute(self.__sql(),\
                            self.__data_pair.get_value()\
                            + self.__key_pair.get_value())

        # clear all the temp data
        self.clear()

        # save the changes
        self.__conn.commit()
        return self
    def clear(self,join = False,col= False):
        # clear the join info
        if join:
            self.__join= []
            self.__join_key =[]
        if col:
            self.__from = []
        # reset the values
        self.__sort_by = []
        self.__operator = "SELECT"
        self.__key_pair.clear()
        self.__data_pair.clear()

        return self

    def __print_exe(self):
        if self.__test:
            # print the essential information of exectuion for debug
            print(self.__sql())
            print(self.__data_pair.get_value()\
                    +self.__key_pair.get_value()+self.__sort_by)
            self.__test = False
    def test_exe(self):
        # debug function
        self.__test  = True
        return self
if __name__ == '__main__':
    __dbName = "../"+ __dbName

    enrol = SqlUtil("enrolments")
    user = SqlUtil("users")
    course = SqlUtil("course")
    print("test find all courses that enroled by user_id = 332")
    user332 = enrol.find("user_id", 332, sign = "=").all()
    print(user332)

    print("\ntest find one course that enroled by user_id = 445")
    user445 = enrol.find("user_id", 445, sign = "=").one()
    print(user445)

    # try the function of join search
    enrol.with_table("users","user_id","id")
    # select one info about comp1521
    print("\ntest join search of users and enrolments table")
    course1521 = enrol.find("course_code", "COMP1521")\
                    .find("course_year","17s2")\
                    .col_name(["user_id","course_code","course_year"])\
                    .col_name("password","users").sort_by("user_id",False)\
                    .test_exe().all()
    for person in course1521:
        print(person)
    print("\nFind one record of year 18s1")
    # select one info about 18s1
    year18s1 = enrol.find("course_year", "18s1").one()
    print (year18s1)

    print("\ntest whether the class works with users table")
    user333 =user.find("id", 333).one()
    print(user333)
    print("\nTest find all the course_code is 1511 and course_year is 17s2 (mutiple criteria search)")
    course1511 = course.find("course_code", "COMP1511").find("course_year","17s2").all()
    print(course1511)


    # Test for insert update and delete

    print("\nTest whether user 1 have record:")
    print(user.find("id",1).all())
    user.insert(["id","password","role"],[1,"toby","test"]).save()

    print("\nTest whether user 1 have recorded:")
    print(user.find("id",1).one())

    print("\nMoidfy the value to name of tecty")
    user.find("id",1).update("password", "tecty").save()
    print(user.find("id",1).one())

    print("\nDelete the inserted item, this sql would execute:")
    user.find("id",1).test_exe().delete()
    print("\nTest whether user 1 have been deleted:")
    print(user.find("id",1).all())



    # # too long to print
    # print("\nTest find all the courses in 17s2")
    # year17s2 = course.find("course_year", "17s2").all()
    # print(year17s2)
