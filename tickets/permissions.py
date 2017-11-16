from rest_framework import permissions


class IsReporter(permissions.BasePermission):
    """
    Custom permission to only allow reporter of ticke.
    """

    def has_object_permission(self, request, view, obj):
        # Permissions are only allowed to the reporter of ticket.
        return obj.reporter == request.user


class IsReporterOrAssignee(permissions.BasePermission):
    """
    Custom permission to only allow  assignee or reporter of the ticket.
    """

    def has_object_permission(self, request, view, obj):
        # Permissions are only allowed to the assignee or reporter of the ticket.
        return obj.assignee == request.user or obj.reporter == request.user

class IsSameUser(permissions.BasePermission):
    """
    Custom permission to only allow if user is trying to access it's own record.
    """

    def has_object_permission(self, request, view, obj):
        # Permissions are only allowed if user is trying to access it's own record.
        return obj == request.user
