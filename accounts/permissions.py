from rest_framework.permissions import BasePermission


class BaseRolePermission(BasePermission):
    def is_staff_user(self, request):
        return request.user.is_staff

    def has_permission(self, request, view):
        return self.is_staff_user(request)


class IsAdmin(BaseRolePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view) or request.user.userprofile.role == 'admin'


class IsSeller(BaseRolePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view) or request.user.userprofile.role == 'seller'


class IsBuyer(BaseRolePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view) or request.user.userprofile.role == 'buyer'
