# Generated by Django 4.2.7 on 2024-07-07 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_photo_file_id_alter_photo_photo_alter_video_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('Женский', 'Женский'), ('Мужской', 'Мужской')], default='Мужской', max_length=7, verbose_name='Гендер'),
        ),
        migrations.AddField(
            model_name='user',
            name='who_looking',
            field=models.CharField(choices=[('Девушек', 'Девушек'), ('Парней', 'Парней')], default='Парней', max_length=7, verbose_name='Кого ищет?'),
        ),
    ]