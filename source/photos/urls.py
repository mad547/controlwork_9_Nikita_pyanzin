from django.urls import path

from photos.views import (
    PhotoListView, PhotoDetailView, PhotoCreateView, PhotoUpdateView, PhotoDeleteView,
    PhotoShareLinkView, PhotoShareView, PhotoFavoriteToggleView,
    AlbumDetailView, AlbumCreateView, AlbumUpdateView, AlbumDeleteView, AlbumFavoriteToggleView,
    FavoritesListView,
)

app_name = 'photos'

urlpatterns = [
    path('', PhotoListView.as_view(), name='index'),
    path('favorites/', FavoritesListView.as_view(), name='favorites'),

    path('photo/create/', PhotoCreateView.as_view(), name='photo_create'),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='photo_detail'),
    path('photo/<int:pk>/edit/', PhotoUpdateView.as_view(), name='photo_edit'),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete'),
    path('photo/<int:pk>/share/', PhotoShareLinkView.as_view(), name='photo_share_link'),
    path('photo/<int:pk>/favorite/', PhotoFavoriteToggleView.as_view(), name='photo_favorite_toggle'),
    path('photo/link/<str:token>/', PhotoShareView.as_view(), name='photo_share'),

    path('album/create/', AlbumCreateView.as_view(), name='album_create'),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name='album_detail'),
    path('album/<int:pk>/edit/', AlbumUpdateView.as_view(), name='album_edit'),
    path('album/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album_delete'),
    path('album/<int:pk>/favorite/', AlbumFavoriteToggleView.as_view(), name='album_favorite_toggle'),
]