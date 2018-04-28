# Golf_Project
Activate Virtual Env - source ./env/bin/activate
Deactivate - deactivate

deleted migration files
-make tables/schema
python3.5 manage.py makemigrations

*Changing Models
1.Run this to update Db based on model change
python3.5 manage.py makemigrations

2.Run this to apply the model changes
python3.5 manage.py migrate


push to heroku

git subtree push --prefix app/golf_project heroku master


