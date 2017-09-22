rm survey.db
cat db/tables.sql | sqlite3 survey.db
python3 db/db_construct.py
