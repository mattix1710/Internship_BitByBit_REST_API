"""
* Serializer needs to be created in order to correctly manage models passed to Response objects
    -> it is because Response objects cannot natively handle complex data types such as Django model instances
"""

from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from master_CS.models import *

#---------------------------------------------------
#-------- PUBLIC ENDPOINT - Course display ---------
#---------------------------------------------------
class ChapterDispSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    
    class Meta:
        model = Chapter
        fields = ['id', 'name', 'desc']
        
class CourseFullDispSerializer(serializers.ModelSerializer):
    chapters = ChapterDispSerializer(many = True)
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'desc', 'instructor', 'chapters']

    # custom update() method for nested representation
    def update(self, instance, validated_data):
        print("VALI_DATA:", validated_data)
        chapters_data = validated_data.pop('chapters')
        instance.name = validated_data.get('name', instance.name)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.instructor = validated_data.get('instructor', instance.instructor)
        instance.save()
        
        for chapter_data in chapters_data:
            print("CHAPTER:", chapter_data['id'])
            try:
                chapter = Chapter.objects.get(pk = chapter_data['id'])
                chapter.name = chapter_data['name']
                chapter.desc = chapter_data['desc']
                chapter.save()
            except ObjectDoesNotExist:
                # if such chapter doesn't yet exist - create new!
                chapter = Chapter.objects.create(name = chapter_data['name'], desc = chapter_data['desc'], course = instance)
                chapter.save()
        return instance
        
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
        fields = ['id', 'name', 'desc', 'instructor']
        
#---------------------------------------------------
#------ PRIVATE ENDPOINT - create new COURSE -------
#---------------------------------------------------
class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['name', 'desc']

class CourseCreateSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many = True)
    class Meta:
        model = Course
        fields = ['name', 'desc', 'chapters']
        
    def create(self, validated_data):
        chapters_data = validated_data.pop('chapters')
        course = Course.objects.create(**validated_data)
        
        for chap in chapters_data:
            Chapter.objects.create(name = chap['name'], desc = chap['desc'], course = course)
        
        return course