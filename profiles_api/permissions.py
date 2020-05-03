from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allows User to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check User is trying to edit own profile or not"""
        
        if request.method in permissions.SAFE_METHODS:
            return True

        else:
            return obj.id == request.user