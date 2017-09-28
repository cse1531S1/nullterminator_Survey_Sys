rm db/survey.db
cat db/tables.sql | sqlite3 db/survey.db
python3 db_construct.py
