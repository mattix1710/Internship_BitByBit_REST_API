from rest_framework.response import Response
from rest_framework.decorators import api_view

# created models
from master_CS.models import Course
from .serializers import CourseSerializer


@api_view(['GET'])
def getData(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)