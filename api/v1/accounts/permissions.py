from rest_framework import permissions



class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            
            return True

        elif request.user.id == obj.id:
            
            return True
            
        return False