from sql_uti import SqlUtil
from survey import Course
import csv

# create an instance of course to find the course id 
c = Course()


enrol = SqlUtil("enrolments")
user = SqlUtil("users")
course = SqlUtil("course")
"""this script only could test once"""
# insert the course database
with open("db/courses.csv",'r') as csv_in:
    reader = csv.reader(csv_in)
    for row in reader:
        # print(row)
        course.insert(["course_code","course_year"],row[:]).save()


# insert the information into database
with open("db/enrolments.csv",'r') as csv_in:
    reader = csv.reader(csv_in)
    for row in reader:
        # print(row)
        this_course = c.get_course(row[1], row[2])
        # append the table by the course_id in course table
        enrol.insert(["user_id","course_id"],[row[0],this_course[0]]).save()

# insert the users database
with open("db/passwords.csv",'r') as csv_in:
    reader = csv.reader(csv_in)
    for row in reader:
        # print(row)
        user.insert(["id","password","role"],row[:]).save()



# print(query.all()) # too much to show, but this is valid
