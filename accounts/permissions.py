from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.userprofile.role == 'admin'


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.userprofile.role == 'seller'


class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        return request.user.userprofile.role == 'buyer'
