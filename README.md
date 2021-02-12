# interview-scheduler

# Python 3

1. Create an environment and activate it
2. Clone the project
3. Checkout to master branch
4. Install requirements.txt using pip
5. python manage.py makemigrations
6. python manage.py migrate
7. python manage.py createsuperuser
8. python manage.py runserver
9. Login to django-admin as superuser
    9.1. Create Roles ('HR','Interviewer','Candidate')
    9.2. Create a Profile for HR
10. Login as HR
    10.1. Create Users
11. Login as 'Interviewer' or 'Candidate' and mark Availability
12. Check Available Time for Interview in HR profile using the Id of 'Interviewer' and 'Candidate'.



NOTE:
I have attached the DB that I used. You can use it or you can delete the db.sqlite3 and run makemigrations and migrate to create new DB.

credentials of my DB

superuser :
username: admin
password: admin@123

HR :
username: anshid
password: admin@123
