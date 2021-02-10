from rest_framework import permissions

MODERATOR_METHODS = ('DELETE',)


class IsOwnerOrSuperuserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.method in MODERATOR_METHODS and
                request.user.is_moderator or
                obj.author == request.user
            )
        )
