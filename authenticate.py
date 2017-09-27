from flask import Flask, redirect, request, render_template, url_for
from flask_login import LoginManager,login_user,current_user,login_required,logout_user
from user import User
from server import app,login_manager
import sqlite3
from db.sql_uti import SqlUtil
from werkzeug.security import check_password_hash,generate_password_hash


def check_password(user_id, password):
    valid = compare_password(user_id, password)
    if valid == True:

        user = User(user_id)
        login_user(user)

        return True
    return False

#Get information about the user from the database
def get_user(user_id):
    new_user = User()
    #User.name(user_id) = get_name(user_id)
    new_user.role = get_role(user_id)

    return new_user


@login_manager.user_loader
def load_user(user_id):
    user = get_user(user_id)
    return user


def compare_password(user_id, password):

    #Query Using sql_util ...

    #connection = sqlite3.connect('user')  #TABLE FOR USER ????
    #c = conn.cursor()
    #c.execute("SELECT * FROM user WHERE id =?", (user_id))
    #con.commit()
    #row = cur.fetchone()
    row = user.findById(user_id)
    #print(row)
    return check_password_hash(password, row[1])

def get_role(user_id):

    #Query Using sql_util ...

    #connection = sqlite3.connect('user')  #TABLE FOR USER ????
    #c = conn.cursor()
    #c.execute("SELECT * FROM user WHERE id =?", (user_id))
    #con.commit()
    #row = cur.fetchone()
    row = user.findById(user_id)
    role = row[2]
    return role





#test authentication
if __name__ == '__main__':

    password = 'secret_password'
    print ("Raw Password: " +  password)
    hash_pass = generate_password_hash(password)
    print ("Hash password: " + hash_pass)
    isvalid = check_password_hash(hash_pass, password)
    print(isvalid)

    password = 'secret_password'
    print ("Raw Password: " +  password)
    hash_pass = generate_password_hash(password)
    print ("Hash password: " + hash_pass)
    password = 'fake_secret'
    isvalid = check_password_hash(hash_pass, password)
    print(isvalid)
