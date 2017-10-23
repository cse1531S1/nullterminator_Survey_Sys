Section-1
python: python 3.5.2
python libraries:
    Flask==0.12.2
    Jinja2==2.8
    Flask-Login==0.4.0
There are some libs are these lib's dependency, more info please check the requirements.txt.

Section-2
When you are in the root folder of this project, run these two command, you can see the website.
# sh init_db.sh
# python3 run.py
You can see the survey system on http://localhost:8080/ or http://YOUR_HOST_IP:8080/

Section-3
Copy all the test files to the root folder(The file struct is supplied at the end.), then type in the command:
# python3 tests.py
Then you are expect to see these result:
|......................
|----------------------------------------------------------------------
|Ran 22 tests in 0.169s
|
|OK

The building database would cost some time.

More info you can checkout the README.md or go to
https://github.com/cse1531S1/nullterminator_Survey_Sys


.:
bin
db
db_construct.py
enrolment.py
file_structure.txt
include
init_db.sh
lib64
local
node_modules
pip-selfcheck.json
__pycache__
question.py
README.md
requirements.txt
respond.py
routes.py
run.py
server.py
share
sql_uti.py
static
survey.py
templates
testEnrolment.py
testQuestion.py
tests.py
testSurvey.py
testUser.py
update.sh
user.py

./bin:
activate
activate.csh
activate.fish
activate_this.py
easy_install
easy_install-2.7
easy_install-3.5
flask
pip
pip2
pip2.7
pip3
pip3.5
python
python2
python2.7
python3
python3.5
python-config
wheel

./db:
courses.csv
enrolments.csv
passwords.csv
survey.db
tables.sql

./include:
python2.7
python3.5m

./local:

./node_modules:

./__pycache__:
csv_uti.cpython-35.pyc
enrolment.cpython-35.pyc
new_question.cpython-35.pyc
new_respond.cpython-35.pyc
new_survey.cpython-35.pyc
question.cpython-35.pyc
respond.cpython-35.pyc
routes.cpython-35.pyc
server.cpython-35.pyc
sql_uti.cpython-35.pyc
survey.cpython-35.pyc
testEnrolment.cpython-35.pyc
testQuestion.cpython-35.pyc
testSurvey.cpython-35.pyc
testUser.cpython-35.pyc
user.cpython-35.pyc

./share:
python-wheels

./share/python-wheels:
CacheControl-0.11.5-py2.py3-none-any.whl
chardet-2.3.0-py2.py3-none-any.whl
colorama-0.3.7-py2.py3-none-any.whl
distlib-0.2.2-py2.py3-none-any.whl
html5lib-0.999-py2.py3-none-any.whl
ipaddress-0.0.0-py2.py3-none-any.whl
lockfile-0.12.2-py2.py3-none-any.whl
packaging-16.6-py2.py3-none-any.whl
pip-8.1.1-py2.py3-none-any.whl
pkg_resources-0.0.0-py2.py3-none-any.whl
progress-1.2-py2.py3-none-any.whl
pyparsing-2.0.3-py2.py3-none-any.whl
requests-2.9.1-py2.py3-none-any.whl
retrying-1.3.3-py2.py3-none-any.whl
setuptools-20.7.0-py2.py3-none-any.whl
six-1.10.0-py2.py3-none-any.whl
urllib3-1.13.1-py2.py3-none-any.whl
wheel-0.29.0-py2.py3-none-any.whl

./static:
bootstrap.min.css
bootstrap.min.js
Chart.min.js
jquery-3.2.1.js
popper.js
style.css
utils.js

./templates:
add_q.html
base.html
comp
dash
del_q.html
final_survey.html
finish_survey.html
index.html
login.html
msg.html
permission.html
register.html
results.html
select_course.html
select_result.html
student.html
success_add_q.html
success_del_q.html
survey_create.html

./templates/comp:
course_list.html
msg.html
q_list.html

./templates/dash:
admin.html
base.html
_enrol_course.html
guest.html
_guest_list.html
_pending_enrol.html
staff.html
student.html
_survey_list.html
_todo_s.html
