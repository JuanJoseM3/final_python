from rest_framework import permissions

class IsLibraryUser(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            return bool(
                request.method in permissions.SAFE_METHODS or
                request.user and
                request.user.is_authenticated
            )
        
class IsRentedToAnother(permissions.BasePermission):        
    def has_object_permission(self, request, view, obj):
        if obj.is_rented:
            if request.user.is_staff:
                return True
            elif request.user == obj.member:
                return True
            else:
                return False
        else:
            if request.user.is_staff:
                return True
            else:
                return False
