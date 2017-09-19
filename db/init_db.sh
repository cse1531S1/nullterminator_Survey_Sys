rm survey.db
cat create_table.sql | sqlite3 survey.db
python3 db_construct.py
