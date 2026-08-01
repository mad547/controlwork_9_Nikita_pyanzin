from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from photos.models import Photo, Album


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


class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'photos/album_detail.html'
    context_object_name = 'album'


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