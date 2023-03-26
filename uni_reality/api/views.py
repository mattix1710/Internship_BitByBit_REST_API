from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.request import Request
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

from django.contrib.auth import authenticate, login, logout

# created models
from master_CS.models import *
from .serializers import CourseSerializer, CourseIdSerializer, CourseFullDispSerializer, StudentSerializer, StudentCoursesSerializer, UserBasicInfoSerializer, ChapterSerializer, LectureSerializer, CourseCreateSerializer
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

# TODO: createCourse
@api_view(['POST'])
@permission_classes([isInstructorOrAdmin])
def createCourse(request):
    if request.user.type != 'INSTRUCTOR':
        return Response({'error': 'Only instructors can create courses'}, status=status.HTTP_403_FORBIDDEN)
    
    course_data = request.data.get('course')
    chapters_data = request.data.get('chapters')
    lectures_data = request.data.get('lectures')
    
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
        chapter = chapter_ser.save()
        for lecture in lectures_data:
            if lecture['chapter'] == chapter.pk:
                #INFO: bezsens - to samo?
                lecture['chapter'] = chapter.pk
                lecture_serializer = LectureSerializer(data = lecture)
                if lecture_serializer.is_valid():
                    lecture_serializer.save()
                else:
                    course.delete()
                    chapter.delete()
                    return Response(lecture_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'message': 'Course, chapters and lectures created successfully'}, status=status.HTTP_201_CREATED)

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
    ],
    "lectures": [
        {
            "title": "Lecture 1 Title",
            "desc": "Lecture 1 Description",
            "recording": "https://example.com/lecture1",
            "chapter": 1
        },
        {
            "title": "Lecture 2 Title",
            "desc": "Lecture 2 Description",
            "recording": "https://example.com/lecture2",
            "chapter": 2
        }
    ]
}
'''
    
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def getCourseDetails(request, *args, **kwargs):
    courses = Course.objects.get(id = kwargs['id'])
    serializer = CourseFullDispSerializer(courses, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
# TODO: updateCourse
@api_view(['PUT'])
@permission_classes([isCourseOwner])
def  updateCourse(request):
    print("Hello")