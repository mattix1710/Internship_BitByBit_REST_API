"""
* Serializer needs to be created in order to correctly manage models passed to Response objects
    -> it is because Response objects cannot natively handle complex data types such as Django model instances
"""

from rest_framework import serializers
from master_CS.models import *

class UserSerializer(serializers.ModelSerializer):
    
    assignedCourses = serializers.PrimaryKeyRelatedField(many=True, queryset=CourseAssignment.objects.all())
    
    class Meta:
        model = User
        fields = ['email', 'name', 'surname', 'assignedCourses']

# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Course
#         fields = '__all__'
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAssignment
        fields = '__all__'
        depth = 2

#---------------------------------------------------
#-------- PUBLIC ENDPOINT - Course display ---------
#---------------------------------------------------

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['title', 'desc', 'recording']

class ChapterSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(many = True)
    
    class Meta:
        model = Chapter
        fields = ['name', 'desc', 'lectures']
        
class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many = True)
    
    class Meta:
        model = Course
        fields = ['name', 'desc', 'instructor', 'chapters']
        
#---------------------------------------------------
#--- PRIVATE ENDPOINT - Assigned Courses display ---
#---------------------------------------------------

class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'desc', 'instructor']

class CourseAssignmentSerializer(serializers.ModelSerializer):
    courses = StudentCourseSerializer()
    
    class Meta:
        model = CourseAssignment
        fields = ['courses']
        depth = 1
        
class StudentCoursesSerializer(serializers.ModelSerializer):
    courses = CourseAssignmentSerializer(many = True, read_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'type', 'courses']
        
#---------------------------------------------------
#---- PRIVATE ENDPOINT - display About Me info -----
#---------------------------------------------------
    
class UserBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'date_joined', 'type']