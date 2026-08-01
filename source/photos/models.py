from django.conf import settings
from django.db import models

# Create your models here.
class Album(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='albums',
        verbose_name='Автор'
    )
    is_private = models.BooleanField(
        default=False,
        verbose_name='Приватный'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'album'
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'
        ordering = ['-created_at']


class Photo(models.Model):
    image = models.ImageField(
        upload_to='photos',
        verbose_name='Фотография'
    )
    caption = models.CharField(
        max_length=255,
        verbose_name='Подпись'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Автор'
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='photos',
        null=True,
        blank=True,
        verbose_name='Альбом'
    )
    is_private = models.BooleanField(
        default=False,
        verbose_name='Приватная'
    )
    share_token = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Токен доступа'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return self.caption

    class Meta:
        db_table = 'photo'
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['-created_at']


class PhotoFavorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_photos',
        verbose_name='Пользователь'
    )
    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Фотография'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        db_table = 'photo_favorite'
        unique_together = ['user', 'photo']
        verbose_name = 'Избранная фотография'
        verbose_name_plural = 'Избранные фотографии'


class AlbumFavorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_albums',
        verbose_name='Пользователь'
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Альбом'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        db_table = 'album_favorite'
        unique_together = ['user', 'album']
        verbose_name = 'Избранный альбом'
        verbose_name_plural = 'Избранные альбомы'