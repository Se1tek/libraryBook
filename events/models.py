from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Event(models.Model):
    FORMAT_CHOICES = [
        ('online', 'Онлайн'),
        ('hybrid', 'Гибридный'),
    ]
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='organized_events', verbose_name='Организатор')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                  null=True, blank=True, verbose_name='Категория')
    book_title = models.CharField(max_length=200, blank=True, verbose_name='Книга')
    book_author = models.CharField(max_length=200, blank=True, verbose_name='Автор книги')
    cover_image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name='Обложка')
    date = models.DateTimeField(verbose_name='Дата и время')
    duration_minutes = models.PositiveIntegerField(default=90, verbose_name='Длительность (мин)')
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='online', verbose_name='Формат')
    stream_link = models.URLField(blank=True, verbose_name='Ссылка на трансляцию')
    max_participants = models.PositiveIntegerField(default=50, verbose_name='Макс. участников')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['date']

    def __str__(self):
        return self.title

    @property
    def participants_count(self):
        return self.registrations.filter(is_confirmed=True).count()

    @property
    def is_upcoming(self):
        return self.date > timezone.now()

    @property
    def is_full(self):
        return self.participants_count >= self.max_participants


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                               related_name='registrations', verbose_name='Мероприятие')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='registrations', verbose_name='Пользователь')
    registered_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Регистрация'
        verbose_name_plural = 'Регистрации'
        unique_together = ('event', 'user')

    def __str__(self):
        return f'{self.user} → {self.event}'


class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                               related_name='comments', verbose_name='Мероприятие')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True,
                                on_delete=models.CASCADE, related_name='replies')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.user}: {self.text[:50]}'
