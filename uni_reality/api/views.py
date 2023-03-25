from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status

from rest_framework.views import APIView

# created models
from master_CS.models import *
from .serializers import CourseSerializer, StudentSerializer

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def getCourses(request: Request):
    print(request.content_type)
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getStudentsCourses(request):
    print(request)
    assignments = CourseAssignment.objects.all()
    serializer = StudentSerializer(assignments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getCourseDetails(request):
    hello =''
    
class StudentsCourses(generics.ListAPIView):
    student_serializer = StudentSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        return Course.objects.filter()
# class CreateCourse(generics.CreateAPIView):
#     def create(self, request, *args, **kwargs):
#         return super().create(request, *args, **kwargs)
        
# class CourseListView(APIView):
#     permission_classes = [permissions.AllowAny,]
    
#     def getCourses(self, request):
#         courses = Course.objects.all()
#         serializer = CourseSerializer(courses, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class CourseListViewAuth(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated,]
    
    # List all courses - GET
    def getCourses(self, request, *args, **kwargs):
        '''
        List all available Courses for given requested user
        '''
        assignmentList = CourseAssignment.objects.filter(student=User.objects.get(pk=User.objects.values('mail').extra(where=["mail='{}'".format(request.user.mail)])[0]['mail']))
        
        # courses = Course.objects.filter(user = request.user.id)
        serializer = StudentSerializer(assignmentList)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Create new course - POST
    def createCourse(self, request, *args, **kwargs):
        '''
        Create new Course with given Chapters and Lectures - only for TEACHER users
        '''
        data = {
            'name': request.data.get('name'),
            'desc': request.data.get('desc'),
            'teacher': request.user.mail
        }
        
        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)