from sql_uti import sql_util,conn
import csv

enrol = sql_util("enrolments")
user = sql_util("users")
course = sql_util("course")
"""this script only could test once"""
# insert the information into database
with open("db/enrolments.csv",'r') as csv_in:
    reader = csv.reader(csv_in)
    for row in reader:
        # print(row)
        enrol.insert(["user_id","course_code","course_year"],row[:]).save()

# insert the users database
with open("db/passwords.csv",'r') as csv_in:
    reader = csv.reader(csv_in)
    for row in reader:
        # print(row)
        user.insert(["user_id","user_name","password"],row[:]).save()


# insert the course database
with open("db/courses.csv",'r') as csv_in:
    reader = csv.reader(csv_in)
    for row in reader:
        # print(row)
        course.insert(["course_code","course_year"],row[:]).save()

# print(query.all()) # too much to show, but this is valid
