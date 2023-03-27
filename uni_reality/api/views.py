from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework import permissions
from rest_framework import status

from django.shortcuts import get_object_or_404

# created models
from master_CS.models import *
from .serializers import CourseSerializer, CourseFullDispSerializer, UserBasicInfoSerializer, CourseCreateSerializer
from .permissions import isInstructorOrAdmin, isOwnerOrReadOnly

# DONE - get_courses_view
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_courses_view(request: Request):
    courses = Course.objects.all()
    serializer = CourseFullDispSerializer(courses, many=True)
    return Response(serializer.data)
    
# DONE - get_my_courses_view
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_my_courses_view(request):
    if request.user.type == 'INSTRUCTOR':
        courses = Course.objects.filter(instructor_id = request.user.email)
    elif request.user.type == 'STUDENT':
        courses = Course.objects.filter(courseassignment__student=User.objects.get(email=request.user.email))
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
# DONE - about_me_view
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def about_me_view(request):
    my_info = User.objects.get(email = request.user.email)
    serializer = UserBasicInfoSerializer(my_info)
    return Response(serializer.data, status=status.HTTP_200_OK)

# DONE - instructor_courses_view
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def instructor_courses_view(request, *args, **kwargs):
    
    #TODO: add exception when the user is NOT as instructor!
    instructor = kwargs['email']
    courses = Course.objects.filter(instructor_id = instructor)
    serializer = CourseFullDispSerializer(courses, many = True)
    print(request)
    return Response(serializer.data, status=status.HTTP_200_OK)

# DONE - get_course_details_view
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_course_details_view(request, *args, **kwargs):
    courses = Course.objects.get(id = kwargs['id'])
    serializer = CourseFullDispSerializer(courses, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

# DONE - create_course_view
@api_view(['POST'])
@permission_classes([isInstructorOrAdmin])
def create_course_view(request):
    if request.user.type != 'INSTRUCTOR':
        return Response({'error': 'Only instructors can create courses'}, status=status.HTTP_403_FORBIDDEN)
    
    course_serializer = CourseCreateSerializer(data = request.data)
    if course_serializer.is_valid():
        course_serializer.save(instructor = request.user)
    else:
        return Response(course_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    return Response({'message': 'Course and chapters created successfully'}, status=status.HTTP_201_CREATED)

'''
EXAMPLE:
------------
{
    "name": "Toys",
    "desc": "Toys for everyone!",
    "chapters": [
        {
            "name": "Chapter 1 Name",
            "desc": "Chapter 1 Description"
        },
        {
            "name": "Chapter 2 Name",
            "desc": "Chapter 2 Description"
        },
        {
            "name": "Chapter 3 Name",
            "desc": "Chapter 3 Description"
        }
    ]
}
'''

# DONE
@api_view(['PUT'])
@permission_classes([isOwnerOrReadOnly, permissions.IsAuthenticated])
def course_update_view(request, *args, **kwargs):
    if request.user.type != 'INSTRUCTOR':
        return Response({'error': 'Only instructors can modify courses'}, status=status.HTTP_403_FORBIDDEN)
    
    curr_course = get_object_or_404(Course, pk=kwargs['id'])
    
    if curr_course.instructor != User.objects.get(email=request.user.email):
        return Response({'error': 'Only owner can modify his courses'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        course = Course.objects.get(pk=kwargs['id'])
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CourseFullDispSerializer(course, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
{
    "id": 12,
    "name": "Toys",
    "desc": "Toys for everyone!",
    "instructor": "m.livingston@uni.com",
    "chapters": [
        {
            "id": 80,
            "name": "Chapter 1 Name",
            "desc": "Chapter 1 Description"
        },
        {
            "id": 81,
            "name": "Chapter 2 Name",
            "desc": "Chapter 2 Description"
        },
        {
            "id": 82,
            "name": "Chapter 3 Circles",
            "desc": "Chapter 3 Description"
        }
    ]
}
'''