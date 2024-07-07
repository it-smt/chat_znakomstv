from django.contrib import admin
from .models import User, Photo, Video


class PhotoInline(admin.TabularInline):
    """Инлайн-представление модели фотографии."""
    model = Photo


class VideoInline(admin.TabularInline):
    """Инлайн-представление модели видео."""
    model = Video


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Представление пользователя в админке."""
    list_display = ['id', 'user_id', 'username', 'first_name', 'last_name', 'age', 'city']
    inlines = [PhotoInline, VideoInline]
