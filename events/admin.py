from django.contrib import admin
from .models import Event, Registration, Comment, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date', 'participants_count', 'is_active']
    list_filter = ['is_active', 'format', 'category']
    search_fields = ['title', 'book_title']

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'registered_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'created_at']
