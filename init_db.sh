rm db/*.db
cat db/tables.sql | sqlite3 db/survey.db
cat db/tables.sql | sqlite3 db/course.db
cat db/tables.sql | sqlite3 db/users.db
python3 db_construct.py
