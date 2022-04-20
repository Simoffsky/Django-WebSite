from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="usersphoto", blank=True)

    def __str__(self):
        return self.user.username





class Friend(models.Model):
    friend1 = models.ForeignKey('Profile', blank=True, related_name='friend1', on_delete=models.CASCADE,null=True)
    friend2 = models.ForeignKey('Profile', blank=True, related_name='friend2',on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'


class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок',blank=True)
    content = models.TextField(blank=True, verbose_name='Текст поста')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    author = models.ForeignKey('Profile',   on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['time_create', 'title']
