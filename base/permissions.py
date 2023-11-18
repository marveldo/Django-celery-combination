from rest_framework.permissions import  BasePermission,SAFE_METHODS

#This is For permissions
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is an admin
        if request.user.is_authenticated:
            return request.user.is_admin 
        else:
            return request.method in SAFE_METHODS
        
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin
        else:
            return False