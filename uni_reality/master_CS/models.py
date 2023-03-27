from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save

# USER model
class User(AbstractUser):
    POSITION_CHOICES = (("STUDENT", "student"), ("INSTRUCTOR", "instructor"), ("ADMIN", "admin"))

    email = models.EmailField(primary_key=True)
    type = models.CharField(max_length=10, choices=POSITION_CHOICES)
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'type', 'password']
    
    def __str__(self):
        return "{} : {}".format(self.type, self.email)
    
def set_permissions_by_type(sender, instance, *args, **kwargs):
    print(instance.type)
    
    if instance.type == 'STUDENT':
        instance.is_superuser = False
        instance.is_staff = False
    if instance.type == 'INSTRUCTOR':
        instance.is_superuser = False
        instance.is_staff = True
    elif instance.type == 'ADMIN':
        instance.is_superuser = instance.is_staff = True
pre_save.connect(set_permissions_by_type, sender=User)
        
# COURSE model
class Course(models.Model):
    name = models.CharField(max_length=50, unique=True)
    desc = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.PROTECT, db_column='instructor', to_field='email')

# junction model linking USER & COURSE models in MANY-to-MANY relationship
class CourseAssignment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
# CHAPTER model (chapter of a COURSE)
class Chapter(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')