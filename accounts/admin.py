from django.contrib import admin
from accounts.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')  # Fields to display in the list view
    search_fields = ('user__username', 'user__email', 'role')  # Fields to search


admin.site.register(UserProfile, UserProfileAdmin)
