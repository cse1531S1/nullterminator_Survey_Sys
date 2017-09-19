from sql_uti import sql_util,conn
import csv

conn.execute("""
create table enrolments (
    user_id int,
    course_code char(8),
    course_year char(4)
);
""")


conn.execute("""
create table users (
    user_id int primary key,
    user_name varchar(20),
    password varchar(255)

);
""")

conn.execute("""
create table course(
    course_code char(8),
    course_year char(4)

);

""")





enrol = sql_util("enrolments")
user = sql_util("users")
course = sql_util("course")
"""this script only could test once"""
# insert the information into database
with open("enrolments.csv",'r') as csv_in:
    reader = csv.reader(csv_in)
    for row in reader:
        # print(row)
        enrol.insert({"user_id":int(row[0]),"course_code":row[1],"course_year":row[2]})
enrol.save()
# insert the users database
with open("passwords.csv",'r') as csv_in:
    reader = csv.reader(csv_in)
    for row in reader:
        # print(row)
        user.insert({"user_id":int(row[0]),"user_name":row[1],"password":row[2]})
user.save()

# insert the course database
with open("courses.csv",'r') as csv_in:
    reader = csv.reader(csv_in)
    for row in reader:
        # print(row)
        course.insert({"course_code":row[0],"course_year":row[1]})
course.save()
# print(query.all()) # too much to show, but this is valid
