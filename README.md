# Survey Website
## Get into development
1. Get into environment
>source bin/activate

2. Run the app
> python run.py

 go to browser for http://localhost:8080/

3. Start working on a new branch
> git checkout -b YOUR_BRANCH_NAME

4. Merge Ur branch <br>
Go to Git Website, start a new [Pull Request](https://github.com/cse1531S1/survey-system-f09a-nullterminator/pulls), after all the teamates have reviewed, then it would merge to master branch.

## User story
All the user story are in [project](https://github.com/cse1531S1/survey-system-f09a-nullterminator/projects/1) page. When ur working on a story, u can drag and drop the card, so the others can know what's left could do.

# Database
## New table
1. Add the initialisation script (in SQL) in file db/tables.sql
2. Run the script by using this command:
>sh init_db.sh
3. Check whether your table have been initialised:
>sqlite3 survey.db <br>
>sqlite3> .tables <br>
>course enrolments users YOUR_NEW_TABLE_NAME

## sql_util("TABLE_NAME")
1. This is a runtime python3 to SQL explainer. Have a lots of great feature:
    - One line execution:
    ```python
    user = sql_util("users")
    # this would select all the information in table users.
    user.all()
    # find one instance of user_id = 50
    user.find("user_id",50).one()
    ```
    - Super Long one line execution example:
    ```python
    course1521 = enrol.find("course_code", "COMP1521")\
                        .find("course_year","17s2")\
                        .col_name(["user_id","course_code","course_year"])\
                        .col_name("user_name","users").all()```
    - Dynamic explaination
    ```python
    # delete the user_id = 50
    user.find("user_id",50).delete()
    # which is same as this line
    user.find("user_id",50).update("user_id",49).save()
    user.update("user_id",49).find("user_id",50).save()
    ```
    - Test execution (for debug). Use test_exe() before the finialise functions, you can see the source SQL after explaination.<br> # this doesn't work for delete()
    ```python
    user.test_exe().all()```
- There is difference between some function. Some function is act like execute the all your data, so these function must put at the end of line, and most of them would stop the online execution.
```python
save() / one() / all() / delete()```
- Some function won't sensetive to the order of how you put it around. These function just to put in neccessary infomation of that SQL execution.
```python
find() / insert() / update() / col_name() / with_table()```
- More example could be seen at user.py and the unit test in db/sql_uti.py

# Layout
## How to use
1. At the template file add a file with these line
    ```
    {% extend "base.html" %}
    {%block title%}CONTENT IN TITILE TAG{%endblock%}
    {% block header %}HEADLING OF A PAGE{% endblock%}
    {%block body%}
    BODY CONTENT OF A PAGE
    {%endblock%}
    ```

## Message
1. Error Success Normal Message:<br>
    When use the render_template(), use these msg_err msg_suc msg_pri variable name to pass in your message.
    ```python
    # here is a quick example
    return render_template("student.html", course_name = name, msg_err = error,\
        quest_list = questionlist,length = length)```



# Write at Last
Have fun and enjoy the experience in flask.
