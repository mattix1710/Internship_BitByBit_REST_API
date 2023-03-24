"""
* Serializer needs to be created in order to correctly manage models passed to Response objects
    -> it is because Response objects cannot natively handle complex data types such as Django model instances
"""

from rest_framework import serializers
from master_CS.models import Course



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'