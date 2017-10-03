from flask import Flask, redirect, request, render_template, url_for
from flask_login import LoginManager,login_user,current_user,login_required,logout_user
#from user import User
from server import app,login_manager,get_db
import sqlite3
from sql_uti import SqlUtil
from werkzeug.security import check_password_hash,generate_password_hash
import csv


def check_password(user_id, password):
    valid = compare_password(user_id, password)
    if valid == True:
        return True
    return False


def compare_password(user_id, password):

    user = SqlUtil("users")
    row = user.find("id",user_id).one()
    hash_pass = row[1]
    return check_password_hash(hash_pass, password)


if __name__ == '__main__':
#    user = SqlUtil("users")
    with app.app_context():

        user = SqlUtil("users")

        print('=== Test Hashing comparison ===')
        password = 'secret_password'
        print ("Raw Password: " +  password)
        hash_pass = generate_password_hash(password)
        print ("Hash password: " + hash_pass)
        isvalid = check_password_hash(hash_pass, password)
        print(isvalid)

        password = 'Correct_password'
        print ("Raw Password: " +  password)
        hash_pass = generate_password_hash(password)
        print ("Hash password: " + hash_pass)
        password = 'wrong_password'
        isvalid = check_password_hash(hash_pass, password)
        print(isvalid)

        print ("==================")
        print("\n\nInserting user into db:")

        hash_pass = generate_password_hash("daniel")
        user.insert(["id","password","role"],[123411111111,hash_pass,"test"]).save()
        print(user.find("id",123411111111).one())

        print("=== Test on known user - valid ===")
        row = user.find("id",123411111111).one()
        print("Compare on correct password")
        isValid = check_password(123411111111,"daniel")
        print(isValid)

        print("\n=== Test on known user - invalid ===")

        row = user.find("id",123411111111).one()
        print("Compare on correct password")
        isValid = check_password(123411111111,"touyhjby")
        print(isValid)


        print("\nDelete the inserted item, this sql would execute:")
        user.find("id",123411111111).test_exe().delete()
        print("\nTest whether user 1 have been deleted:")
        print(user.find("id",123411111111).all())
    #################################
