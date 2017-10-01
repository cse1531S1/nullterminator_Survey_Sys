from sql_uti import SqlUtil,conn
import csv
from werkzeug_security import generate_password_hash,check_password_hash

enrol = SqlUtil("enrolments")
user = SqlUtil("users")
course = SqlUtil("course")
"""this script only could test once"""
# insert the information into database
with open("db/enrolments.csv",'r') as csv_in:
    reader = csv.reader(csv_in)
    for row in reader:
        # print(row)
        row = row.split(',')
        enrol.insert(["user_id","course_code","course_year"],[(int)row[0], row[1], row[2]]).save()

# insert the users database
#Uses Hash security to store passwords
with open("db/passwords.csv",'r') as csv_in:
    reader = csv.reader(csv_in)
    for row in reader:
        # print(row)
        row = row.split(',')
        #Generate hash for the password
        row[1] = generate_password_hash(row[1])
        user.insert(["id","password","role"],[(int)row[0], row[1], row[2]]).save()


# insert the course database
with open("db/courses.csv",'r') as csv_in:
    reader = csv.reader(csv_in)
    for row in reader:
        # print(row)
        course.insert(["course_code","course_year"],row[:]).save()

# print(query.all()) # too much to show, but this is valid
