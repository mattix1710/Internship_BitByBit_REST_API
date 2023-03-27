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
## Proposed reality
* There are 3 main models
  * **User** - can be a type {student/instructor/admin}
  * **Course** - students can be assigned to them and instructors can be owners of the course
  * **Chapter** - chapters of a course (relationship 1-N with Course)
* There is 1 helper model
  * **CourseAssignment** - holds relationship between **User** and **Course** in many-to-many way
    * Each **User** can be assigned to many **Courses**
    * Each **Course** can be assigned to many **Users**

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