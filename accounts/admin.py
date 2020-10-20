from django.contrib import admin

from .models import User
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'last_name', 'first_name', 'gender', 'updated_time', 'last_login']
