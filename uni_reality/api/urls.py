from django.urls import path

from . import views

urlpatterns = [
    path('api/courses/', views.getCourses),
    path('api/student/', views.aboutMe),
    path('api/courses/my-courses/', views.getMyCourses),
    path('api/courses/instructor/<str:email>/', views.instructorCourses),
    path('api/courses/create/', views.createCourse),
    path('api/courses/<str:id>/', views.getCourseDetails),
    path('api/courses/<str:id>/update/', views.course_update_view),
]