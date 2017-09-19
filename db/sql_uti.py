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
        sql+= "FROM "+ self.__table_name + ""
        if self.__search_key:
            # have specific some value to search
            sql += " where "
            sql += " and ".join(self.__search_key)

        # end of the sql sentense
        sql +=";"

        #  clear all the list have been use
        self.__from = []
        self.__search_key = []
        return sql

    def col_name(self, col):
        self.__from.append(col)
        return self
    def all(self):
        # convey the varable setted to a valid sql sentense and query the
        # database, collect the result and resent back the data

        return self.__conn.execute(self.__sql()).fetchall()


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
    def one(self):
        return self.__conn.execute(self.__sql()).fetchone()


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
    def save(self):
        # save all the changes into database
        # save the changes
        self.__conn.commit()
        return self

if __name__ == '__main__':
    query = sql_util("enrolments")
    user = sql_util("users")
    course = sql_util("course")


    user332 = query.find("user_id", 332, sign = "=").all()
    print(user332)
    user445 = query.find("user_id", 445, sign = "=").one()
    print(user445)
    user333 =user.find("user_id", 333).one()
    print(user333)


    course1511 = course.find("course_code", "COMP1511").find("course_year","17s2").all()
    print(course1511)

    year17s2 = course.find("course_year", "17s2").all()
    print(year17s2)
