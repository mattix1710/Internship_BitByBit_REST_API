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
    
class isOwnerOrReadOnly(permissions.BasePermission):
    '''
    Custom permission to only allow OWNER of the course
    '''
    
    # def has_permission(self, request, view, obj):
    #     if request.user.is_anonymous:
    #         return False
    #     if request.user.type != 'INSTRUCTOR':
    #         return False
    #     if request.user != obj.instructor:
    #         return False
    #     return True
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the course.
        return obj.instructor == request.user