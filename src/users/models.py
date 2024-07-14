from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import generate_secret_token


class User(AbstractUser):
    """Кастомная модель пользователя."""

    class Gender(models.TextChoices):
        """Гендер пользователя."""
        FEMALE = 'Женский', 'Женский'
        MALE = 'Мужской', 'Мужской'

    class WhoLooking(models.TextChoices):
        """Кого ищет пользователь."""
        FEMALE = 'Девушек', 'Девушек'
        MALE = 'Парней', 'Парней'
        ALL = 'Без разницы', 'Без разницы'

    user_id = models.IntegerField(unique=True, verbose_name='ID пользователя телеграмм', blank=True, null=True)
    age = models.PositiveIntegerField(verbose_name='Возраст', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    city = models.CharField(max_length=255, verbose_name='Город', blank=True, null=True)
    auth_token = models.CharField(max_length=256, verbose_name='Токен авторизации', blank=True, null=True)
    gender = models.CharField(max_length=7, verbose_name='Гендер', choices=Gender.choices, default=Gender.MALE)
    who_looking = models.CharField(max_length=11, verbose_name='Кого ищет?', choices=WhoLooking.choices,
                                   default=WhoLooking.MALE)

    class Meta(AbstractUser.Meta):
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.user_id} {self.get_full_name()}'

    def get_full_name(self):
        return f'{self.username} - {self.first_name}'

    def save(self, *args, **kwargs):
        self.auth_token = generate_secret_token()
        super(User, self).save(*args, **kwargs)


class Photo(models.Model):
    """Модель фотографии пользователя."""
    file_id = models.TextField(verbose_name='ID фото', blank=True, null=True)
    photo = models.ImageField(verbose_name='Фото', upload_to='users/photo/', blank=True, null=True)
    user = models.ForeignKey(verbose_name='Пользователь', to=User, related_name='photos', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return f'{self.user.username} - фото'


class Video(models.Model):
    """Модель видео пользователя."""
    video = models.FileField(verbose_name='Видео', upload_to='users/video/', blank=True, null=True)
    user = models.ForeignKey(verbose_name='Пользователь', to=User, related_name='videos', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        return f'{self.user.username} - видео'
    

class Complaint(models.Model):
    """Модель жалобы."""
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='my_complaints', verbose_name='Обратившийся пользователь')
    accused_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='my_accusations', verbose_name='Обвиняемый пользователь')
    description = models.TextField(verbose_name='Текст с информацией о нарушении')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'

    def __str__(self) -> str:
        return f'Жалоба на {self.accused_user.username} от {self.user.username}'
