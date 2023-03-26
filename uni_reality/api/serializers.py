"""
* Serializer needs to be created in order to correctly manage models passed to Response objects
    -> it is because Response objects cannot natively handle complex data types such as Django model instances
"""

from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from master_CS.models import *

class UserSerializer(serializers.ModelSerializer):
    
    assignedCourses = serializers.PrimaryKeyRelatedField(many=True, queryset=CourseAssignment.objects.all())
    
    class Meta:
        model = User
        fields = ['email', 'name', 'surname', 'assignedCourses']
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAssignment
        fields = '__all__'
        depth = 2

#---------------------------------------------------
#-------- PUBLIC ENDPOINT - Course display ---------
#---------------------------------------------------
class ChapterDispSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'name', 'desc']
        
class CourseFullDispSerializer(serializers.ModelSerializer):
    chapters = ChapterDispSerializer(many = True)
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'desc', 'instructor', 'chapters']
        
    def update(self, instance, validated_data):
        print("VAL_DATA_type", type(validated_data))
        chapters_data = validated_data.pop('chapters')
        instance.name = validated_data.get('name', instance.name)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.instructor = validated_data.get('instructor', instance.instructor)
        instance.save()
        
        for chapter_data in chapters_data:
            print("DATA:",chapter_data)
            try:
                chapter = Chapter.objects.get(id = chapter_data.get('id'))
                chapter.name = chapter_data['name']
                chapter.desc = chapter_data['desc']
                chapter.save()
            except ObjectDoesNotExist:
                # if such chapter doesn't yet exist - create new!
                chapter = Chapter.objects.create(name = chapter_data['name'], desc = chapter_data['desc'], course = instance)
                chapter.save()
        return instance
        
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
        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'desc', 'instructor']
        
class CourseIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'desc', 'instructor']
        
#---------------------------------------------------
#------ PRIVATE ENDPOINT - create new COURSE -------
#---------------------------------------------------
class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'

class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'desc']