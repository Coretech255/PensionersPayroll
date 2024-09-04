from django.contrib import admin
from .models import CustomUser, Profile
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)

