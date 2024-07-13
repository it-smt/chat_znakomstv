from django.contrib import admin
from .models import User, Photo, Video, Complaint


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


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    """Представление жалобы в админке."""
    list_display = ['id', 'user', 'accused_user', 'date_created']
    list_filter = ['date_created', 'user__age', 'user__city', 'user__gender', 'accused_user__age', 'accused_user__city', 'accused_user__gender']
    search_fields = ['user__username', 'user__user_id', 'user__id', 'accused_user__username', 'accused_user__user_id', 'accused_user__id', 'description']
