from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Owner Only Permission."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
