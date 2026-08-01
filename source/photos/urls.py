from django.urls import path

from photos.views import (
    PhotoListView, PhotoDetailView, PhotoCreateView, PhotoUpdateView, PhotoDeleteView,
    AlbumDetailView, AlbumCreateView, AlbumUpdateView, AlbumDeleteView,
)

app_name = 'photos'

urlpatterns = [
    path('', PhotoListView.as_view(), name='index'),

    path('photo/create/', PhotoCreateView.as_view(), name='photo_create'),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='photo_detail'),
    path('photo/<int:pk>/edit/', PhotoUpdateView.as_view(), name='photo_edit'),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete'),

    path('album/create/', AlbumCreateView.as_view(), name='album_create'),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name='album_detail'),
    path('album/<int:pk>/edit/', AlbumUpdateView.as_view(), name='album_edit'),
    path('album/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album_delete'),
]