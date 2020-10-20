from django.contrib import admin

from .models import User, Box
from posts.models import Tag
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'last_name', 'first_name', 'gender', 'updated_time', 'last_login']
    list_filter = ['gender', 'is_superuser']
    ordering = ['-is_superuser']
    fields = ['username', 'password', ('first_name', 'last_name'), 'email',
              'gender', 'phone', 'birthday',
              ('is_superuser', 'is_staff', 'is_active')]


class BoxInline(admin.TabularInline):
    model = Tag.boxes.through


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ['owner']
    inlines = [BoxInline]
