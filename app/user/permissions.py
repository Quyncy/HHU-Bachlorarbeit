from rest_framework import permissions

class AdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        admin_perm = bool(request.user.is_staff and request.user)
        # super().has_permission(request, view)
        return request.method=='GET' or admin_perm


class TutorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.is_tutor == request.user.is_tutor
        # return super().has_object_permission(request, view, obj)
    