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

## Database
### New table
1. Add the initialisation script (in SQL) in file db/tables.sql
2. Run the script by using this command (in db folder):
>sh init_db.sh
3. Check whether your table have been initialised:
>sqlite3 survey.db <br>
>sqlite3> .tables <br>
>course enrolments users YOUR_NEW_TABLE_NAME

## Write at Last
Have fun and enjoy the experience in flask.
