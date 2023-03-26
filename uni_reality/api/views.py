from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.request import Request
from rest_framework import permissions
from rest_framework import status
from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

from django.shortcuts import get_object_or_404

# created models
from master_CS.models import *
from .serializers import CourseSerializer, CourseIdSerializer, CourseFullDispSerializer, StudentSerializer, StudentCoursesSerializer, UserBasicInfoSerializer, ChapterSerializer, CourseCreateSerializer
from .permissions import isInstructorOrAdmin, isCourseOwner

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def getCourses(request: Request):
    # print(request.content_type)
    courses = Course.objects.all()
    serializer = CourseFullDispSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getStudentsCourses(request):
    assignments = CourseAssignment.objects.all()
    serializer = StudentSerializer(assignments, many=True)
    return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getMyCourses(request):
    
    # courses = CourseAssignment.objects.filter(student = request.user.email)
    # serializer = StudentCoursesSerializer(courses)
    if request.user.type == 'INSTRUCTOR':
        courses = Course.objects.filter(instructor_id = request.user.email)
        serializer = CourseIdSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_204_NO_CONTENT)
    # print(request.user.data)
    
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def aboutMe(request):
    my_info = User.objects.get(email = request.user.email)
    serializer = UserBasicInfoSerializer(my_info)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def instructorCourses(request, *args, **kwargs):
    
    #TODO: add exception when the user is NOT as instructor!
    instructor = kwargs['email']
    courses = Course.objects.filter(instructor_id = instructor)
    serializer = CourseSerializer(courses, many = True)
    print(request)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def getCourseDetails(request, *args, **kwargs):
    courses = Course.objects.get(id = kwargs['id'])
    serializer = CourseFullDispSerializer(courses, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([isInstructorOrAdmin])
def createCourse(request):
    if request.user.type != 'INSTRUCTOR':
        return Response({'error': 'Only instructors can create courses'}, status=status.HTTP_403_FORBIDDEN)
    
    course_data = request.data.get('course')
    chapters_data = request.data.get('chapters')
    
    course_serializer = CourseCreateSerializer(data = course_data)
    if course_serializer.is_valid():
        course = course_serializer.save(instructor = request.user)
    else:
        return Response(course_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    chapter_serializers = []
    for chapter in chapters_data:
        chapter['course'] = course.pk
        chapter_serializer = ChapterSerializer(data = chapter)
        if chapter_serializer.is_valid():
            chapter_serializers.append(chapter_serializer)
        else:
            course.delete()
            return Response(chapter_serializer.erorrs, status = status.HTTP_400_BAD_REQUEST)
    
    for chapter_ser in chapter_serializers:
        # chapter = chapter_ser.save()
        chapter_ser.save()
    
    return Response({'message': 'Course and chapters created successfully'}, status=status.HTTP_201_CREATED)

'''
EXAMPLE:
---------
{
    "course": {
        "name": "New Course Name",
        "desc": "New Course Description"
    },
    "chapters": [
        {
            "name": "Chapter 1 Name",
            "desc": "Chapter 1 Description"
        },
        {
            "name": "Chapter 2 Name",
            "desc": "Chapter 2 Description"
        }
    ]
}
'''
    
    
# TODO: almost DONE - updateCourse
@api_view(['PUT'])
@permission_classes([isCourseOwner])
def updateCourse(request, *args, **kwargs):
    # INFO: probably this IF will never be executed - due to permission_class checks
    if request.user.type != 'INSTRUCTOR':
        return Response({'error': 'Only instructors can modify courses'}, status=status.HTTP_403_FORBIDDEN)
    
    curr_course = get_object_or_404(Course, pk=kwargs['id'])
    
    if curr_course.instructor != User.objects.get(email=request.user.email):
        return Response({'error': 'Only owner can modify his courses'}, status=status.HTTP_403_FORBIDDEN)
    
    print(request.data.get('course'))
    print(request.data.get('chapters'))
    
    course_data = request.data.get('course')
    chapters_data = request.data.get('chapters')
    
    course_data['instructor'] = request.user
    
    course_serializer = CourseSerializer(data = course_data)
    if course_serializer.is_valid():
        course = course_serializer.update()
    else:
        return Response(course_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    chapter_serializers = []
    for chapter in chapters_data:
        chapter['course'] = course.pk
        chapter_serializer = ChapterSerializer(data = chapter)
        if chapter_serializer.is_valid():
            chapter_serializers.append(chapter_serializer)
        else:
            return Response(chapter_serializer.erorrs, status = status.HTTP_400_BAD_REQUEST)
    
    for chapter_ser in chapter_serializers:
        chapter_ser.update()
    
    return Response({'message': 'Course and chapters created successfully'}, status=status.HTTP_201_CREATED)

'''
{
    "id": 11,
    "name": "New Course Name",
    "desc": "New Course Description",
    "instructor": "m.livingston@uni.com",
    "chapters": [
        {
            "id": 51,
            "name": "Chapter 1 Name",
            "desc": "Chapter 1 Description"
        },
        {
            "id": 52,
            "name": "Chapter 2 Name",
            "desc": "Chapter 2 Description"
        },
        {
            "name": "Chapter No3",
            "desc": "Chapter 3 Description"
        }
    ]
}


{
    "course": {
        "name": "New Course Name",
        "desc": "New Course Description"
    },
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
            "name": "Chapter No3",
            "desc": "Chapter 3 Description"
        }
    ]
}
'''

@api_view(['PUT'])
@permission_classes([isCourseOwner])
def course_update_view(request, *args, **kwargs):
    try:
        course = Course.objects.get(pk=kwargs['id'])
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    print(request.data)
    serializer = CourseFullDispSerializer(course, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CourseUpdateView(generics.UpdateAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseFullDispSerializer
#     lookup_field = 'id'
    
#     def perform_update(self, serializer):
#         course = serializer.validated_data.get('course')
        
        
#         return super().perform_update(serializer)