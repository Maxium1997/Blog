from django.contrib import admin

from .models import Post, Tag, Comment
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_public', 'creator']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['source_id', 'commenter', 'email', 'content']
