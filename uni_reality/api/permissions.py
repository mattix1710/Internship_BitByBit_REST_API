from rest_framework import permissions

class isInstructorOrAdmin(permissions.BasePermission):
    '''
    Custom permission to only allow INSTRUCTORS or ADMINS for creating a Course
    '''
    
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.method == 'POST' and request.user.type != 'INSTRUCTOR':
            return False    # Only instructors can create new courses
        return True         # Read-only permissions are allowed to anyone
    
class isCourseOwner(permissions.BasePermission):
    '''
    Custom permission to only allow OWNER of the course
    '''
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        if request.user.type != 'INSTRUCTOR':
            return False
        if obj.course not in request.user.course_set.all():
            return False
        return True