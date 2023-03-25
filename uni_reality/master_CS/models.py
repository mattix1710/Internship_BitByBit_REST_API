from django.db import models

# USER model
class User(models.Model):
    POSITION_CHOICES = (("STUDENT", "student"), ("TEACHER", "teacher"), ("ADMIN", "admin"))
    
    mail = models.EmailField(primary_key=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    password = models.CharField(max_length=40)       # stored as SHA1 hash function
    type = models.CharField(max_length=7, choices=POSITION_CHOICES)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

# COURSE model
class Course(models.Model):
    name = models.CharField(max_length=50, unique=True)
    desc = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.PROTECT, db_column='teacher', to_field='mail')
    
class CourseAssignment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
# CHAPTER model (chapter of a COURSE)
class Chapter(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

# TODO: probably delete this model
class Lecture(models.Model):
    title = models.CharField(max_length=50)
    desc = models.TextField()
    recording = models.URLField()
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)