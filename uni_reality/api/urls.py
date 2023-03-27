from django.urls import path

from . import views

urlpatterns = [
    path('api/courses/', views.get_courses_view),
    path('api/my-info/', views.about_me_view),
    path('api/courses/my-courses/', views.get_my_courses_view),
    path('api/courses/instructor/<str:email>/', views.instructor_courses_view),
    path('api/courses/create/', views.create_course_view),
    path('api/courses/<str:id>/', views.get_course_details_view),
    path('api/courses/<str:id>/update/', views.course_update_view),
]