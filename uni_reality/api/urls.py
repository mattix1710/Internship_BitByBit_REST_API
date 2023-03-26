from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    path('api/courses/', views.getCourses),
    path('api/student/', views.aboutMe),
    path('api/courses/my-courses/', views.getMyCourses),
    path('api/courses/instructor/<str:email>/', views.instructorCourses),
]