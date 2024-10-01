from rest_framework.permissions import BasePermission, IsAuthenticated


class BaseRolePermission(BasePermission):
    def is_staff_user(self, request):
        return request.user.is_staff

    def has_permission(self, request, view):
        return self.is_staff_user(request)


class IsAdmin(BaseRolePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return IsAuthenticated and super().has_permission(request, view) or request.user.userprofile.role == 'admin'
        return False


class IsSeller(BaseRolePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return IsAuthenticated and (super().has_permission(request, view) or request.user.userprofile.role == 'seller')
        return False


class IsBuyer(BaseRolePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return IsAuthenticated and super().has_permission(request, view) or request.user.userprofile.role == 'buyer'
        return False