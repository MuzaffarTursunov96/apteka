from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import *



class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'username','viloyat')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

# admin.site.register(User, CustomUserAdmin)
admin.site.register(User)
# admin.site.register(User,CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(Viloyatlar)
