from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from hashlib import sha1
from django.db.models.signals import pre_save

##################################################
################## UserManager ###################
##################################################

# def validate_user_exist(email):
#     try:
#         email_match = User.objects.get(email=email)
#     except User.DoesNotExist:
#         return True
#     raise ValueError("User with such email already exists!")

# class CustomUserManager(UserManager):
#     def create_user(self, email, first_name, last_name, type, password):
#         """
#         Creates and saves a User with the given email and password
#         """
#         if not email:
#             raise ValueError("User must have an email")
        
#         while(1):
#             if validate_user_exist(email):
#                 break
        
#         if not password:
#             raise ValueError("User must have a password")
#         if not first_name:
#             raise ValueError("User must have a first name")
#         if not last_name:
#             raise ValueError("User must have a last name")
        
        
#         user = User(email=email, first_name=first_name, last_name=last_name, type=type, password=password)
            
            
    
#     def create_superuser(self, username: str, email: Optional[str], password: Optional[str], **extra_fields: Any):
#         pass

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

# TODO: probably delete this model
class Lecture(models.Model):
    title = models.CharField(max_length=50)
    desc = models.TextField()
    recording = models.URLField()
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lectures')