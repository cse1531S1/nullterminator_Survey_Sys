rm survey.db
cat tables.sql | sqlite3 survey.db
python3 db_construct.py
