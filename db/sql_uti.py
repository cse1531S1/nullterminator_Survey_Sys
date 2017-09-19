import sqlite3
import csv

# config of the database name
__dbName = "survey.db"

# db connection
conn = sqlite3.connect(__dbName)

class sql_util(object):
    """docstring for sql_util."""
    def __init__(self, table_name):
        super(sql_util, self).__init__()
        self.__conn = conn
        self.__table_name = table_name;
        # sql sentense to change the database
        self.__change  = []
        # colomn that would selected by this query
        self.__from = []
        # keyword for searching
        self.__search_key = []
        # join search for another table
        self.__join = []
        # specify key for join
        self.__join_key = []

    def __where(self):
        # resolve the where sentense
        return " WHERE "+" and ".join(self.__join_key+self.__search_key)

    def __sql(self):
        # generate the sql sentense
        sql = "SELECT"
        if self.__from:
            # has define some col
            sql += " "
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

        if self.__search_key:
            # have specific some value to search
            sql += self.__where()
        # end of the sql sentense
        sql +=";"


        #  clear all the list have been used
        self.__from = []
        self.__search_key = []
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

    def find(self, col, key_word, sign = "="):
        # set the this criteria into the variable
        where = ""+ col +" "+ sign +" "



        if type(key_word) == int:
            #  the key_word is int not need to add"", but it need to convey type
            where += str(key_word)
        else:
            #  key_word is string, need to add ""
            where += "\""+key_word+"\""

        # append this filter to the list
        self.__search_key.append(where)
        return self

    # insert part (low level function)
    def insert(self, values ):
        if type(values)!= dict:
            # the input values must be a dictionary
            raise TypeError
        sql = "INSERT INTO %s (" % self.__table_name
        sql += ",".join(values.keys())
        sql += " ) VALUES ("
        # at the sting value add "" around it
        str_val = []
        for val in values.values():
            if type(val) == str:
                str_val.append("\"%s\"" % val)
            elif type(val) == int:
                # the input type is int, convey it to string
                str_val.append(str(val))
            else:
                # couldn't identify the type of value
                raise TypeError
        sql += ",".join(str_val)

        # end of the sql
        sql += ");"
        # print(sql)
        # append the change into change list
        self.__conn.execute(sql)
        return self

    def one(self):
        return self.__conn.execute(self.__sql()).fetchone()

    def all(self):
        # convey the varable setted to a valid sql sentense and query the
        # database, collect the result and resent back the data

        return self.__conn.execute(self.__sql()).fetchall()
    def save(self):
        # save all the changes into database
        # save the changes
        self.__conn.commit()
        return self

if __name__ == '__main__':
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
    # # too long to print
    # print("\nTest find all the courses in 17s2")
    # year17s2 = course.find("course_year", "17s2").all()
    # print(year17s2)
