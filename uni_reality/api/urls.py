from django.urls import path

from . import views

urlpatterns = [
    path('api/courses/', views.getCourses),
    path('api/student/', views.getStudentsCourses),
    path('api/', views.CourseListViewAuth.as_view()),
]