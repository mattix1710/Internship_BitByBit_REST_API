# Internship_BitByBit
Simple Django project for internship in The BitByBit company

***
## STARTING THE SERVER
* **Starting the server itself**
    > py manage.py runserver
* **creating admin account**
    > py manage.py createsuperuser<br>
    > Username: admin<br>
    > Email address: \<some_email\><br>
    > Password: \<some_password\><br>
* **creating database**
    > py manage.py migrate<br>
    > py manage.py makemigrations<br>

***
## Current Python dependencies
* Python 3.11.0
* Django 4.1.7
* Django REST framework 3.14.0

***
## Available API entries

### PUBLIC
* **`api/courses/`** - [GET] - display all courses
* **`api/courses/instructor/<str:email>/`** - [GET] - display all courses of given *instructor*
* **`api/courses/<str:id>/`** - [GET] - display details of given course

### PRIVATE
* **`api/my-info/`** - [GET] - get information about currently logged in user
* **`api/courses/my-courses/`** - [GET] - list all courses to which STUDENT is assigned OR which owner is INSTRUCTOR

### ONLY FOR INSTRUCTORS (superusers)
* **`api/courses/create/`** - [POST] - create new course
* **`api/courses/<str:id>/update/`** - [PUT] - update course only if current user is the owner