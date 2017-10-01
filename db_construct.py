from sql_uti import SqlUtil
from server import app
import csv

with app.app_context():
    enrol = SqlUtil("enrolments")
    user = SqlUtil("users")
    course = SqlUtil("course")
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
            hash_pass = generate_password_hash(row[1])
            user.insert(["id","password","role"],[row[0], hash_pass, row[2]]).save()


    # insert the course database
    with open("db/courses.csv",'r') as csv_in:
        reader = csv.reader(csv_in)
        for row in reader:
            # print(row)
            course.insert(["course_code","course_year"],row[:]).save()

    # print(query.all()) # too much to show, but this is valid
