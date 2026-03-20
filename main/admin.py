from django.contrib import admin

from .models import Contact, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'likes', 'views', 'link')
    search_fields = ('title', 'description')
    list_filter = ('likes', 'views')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('created_at',)
