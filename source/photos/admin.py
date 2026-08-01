from django.contrib import admin

from photos.models import Album, Photo, PhotoFavorite, AlbumFavorite


# Register your models here.
admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(PhotoFavorite)
admin.site.register(AlbumFavorite)