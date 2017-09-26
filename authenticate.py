from flask import Flask, redirect, request, render_template, url_for
from flask_login import LoginManager,login_user,current_user,login_required,logout_user
from model import User
from server import app,LoginManager
import sqlite3

#load data from passwords csv into the database
def load_passwords(file):



#ALready being done in db_construct ???? 

def check_password(user_id, password):
    valid = find_password(password)
    if valid == True:

        user = User(user_id)
        login_user(user)

        return True
    return False

#Get information about the user from the database
def get_user(user_id):

    User.name(user_id) = get_name(user_id)
    User.role(user_id) = get_role(user_id)

    return User(user_id)


@login_manager.user_loader
def load_user(user_id):
    user = get_user(user_id)
    return user




def get_role(user_id):

    connection = sqlite3.connect('survey.db')  #TABLE FOR USER ????
    c = conn.cursor()
    c.execute("SELECT role FROM survey.db WHERE id =?", (user_id))
    con.commit()
    row = cur.fetchone()
    role = row[2]
    #Retrieve name from the database

    return role
    #retrieve role from the database

    return role
