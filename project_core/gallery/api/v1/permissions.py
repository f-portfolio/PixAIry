from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.publisher.user == request.user
    

class IsOwnerOrSupervisor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.publisher == request.user.profile or request.user.is_supervisor 


class IsGetOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True


class IsSupervisor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_supervisor


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsOwnerCommentOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return (obj.user == request.user.profile) or \
               (obj.blog_post.publisher.user.profile == request.user.profile)
    

