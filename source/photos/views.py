import secrets

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from photos.models import Photo, Album, PhotoFavorite, AlbumFavorite


# Create your views here.
class AuthorOrPermissionMixin(UserPassesTestMixin):
    permission_required = None

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.has_perm(self.permission_required)


class PhotoListView(ListView):
    model = Photo
    template_name = 'photos/index.html'
    context_object_name = 'photos'
    paginate_by = 12

    def get_queryset(self):
        return Photo.objects.filter(is_private=False).select_related('author', 'album')


class PhotoDetailView(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'photos/photo_detail.html'
    context_object_name = 'photo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_has_favorited'] = PhotoFavorite.objects.filter(
            user=self.request.user, photo=self.object
        ).exists()
        return context


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['image', 'caption', 'album', 'is_private']
    template_name = 'photos/photo_create.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['album'].queryset = Album.objects.filter(author=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.album and form.instance.album.is_private:
            form.instance.is_private = True
        return super().form_valid(form)


class PhotoUpdateView(LoginRequiredMixin, AuthorOrPermissionMixin, UpdateView):
    model = Photo
    fields = ['image', 'caption', 'album', 'is_private']
    template_name = 'photos/photo_create.html'
    permission_required = 'photos.change_photo'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['album'].queryset = Album.objects.filter(author=self.request.user)
        return form

    def form_valid(self, form):
        if form.instance.album and form.instance.album.is_private:
            form.instance.is_private = True
        return super().form_valid(form)


class PhotoDeleteView(LoginRequiredMixin, AuthorOrPermissionMixin, DeleteView):
    model = Photo
    template_name = 'photos/photo_confirm_delete.html'
    success_url = reverse_lazy('photos:index')
    permission_required = 'photos.delete_photo'


class PhotoShareLinkView(LoginRequiredMixin, View):

    def post(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk, author=request.user)
        if not photo.share_token:
            photo.share_token = secrets.token_urlsafe(24)
            photo.save()
        return redirect('photos:photo_detail', pk=photo.pk)


class PhotoShareView(DetailView):
    model = Photo
    template_name = 'photos/photo_detail.html'
    context_object_name = 'photo'
    slug_field = 'share_token'
    slug_url_kwarg = 'token'


class PhotoFavoriteToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        favorite = PhotoFavorite.objects.filter(user=request.user, photo=photo)
        if favorite.exists():
            favorite.delete()
            is_favorite = False
        else:
            PhotoFavorite.objects.create(user=request.user, photo=photo)
            is_favorite = True
        return JsonResponse({'is_favorite': is_favorite})


class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'photos/album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_has_favorited'] = AlbumFavorite.objects.filter(
            user=self.request.user, album=self.object
        ).exists()
        return context


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    fields = ['title', 'description', 'is_private']
    template_name = 'photos/album_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AlbumUpdateView(LoginRequiredMixin, AuthorOrPermissionMixin, UpdateView):
    model = Album
    fields = ['title', 'description', 'is_private']
    template_name = 'photos/album_create.html'
    permission_required = 'photos.change_album'

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance.is_private:
            form.instance.photos.update(is_private=True)
        return response


class AlbumDeleteView(LoginRequiredMixin, AuthorOrPermissionMixin, DeleteView):
    model = Album
    template_name = 'photos/album_confirm_delete.html'
    success_url = reverse_lazy('photos:index')
    permission_required = 'photos.delete_album'


class AlbumFavoriteToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        album = get_object_or_404(Album, pk=pk)
        favorite = AlbumFavorite.objects.filter(user=request.user, album=album)
        if favorite.exists():
            favorite.delete()
            is_favorite = False
        else:
            AlbumFavorite.objects.create(user=request.user, album=album)
            is_favorite = True
        return JsonResponse({'is_favorite': is_favorite})


class FavoritesListView(LoginRequiredMixin, ListView):
    template_name = 'photos/favorites.html'
    context_object_name = 'favorite_photos'

    def get_queryset(self):
        return Photo.objects.filter(favorited_by__user=self.request.user, is_private=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite_albums'] = Album.objects.filter(favorited_by__user=self.request.user, is_private=False)
        return context