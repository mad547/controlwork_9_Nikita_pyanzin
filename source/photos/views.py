from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import response
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from photos.models import Photo, Album


# Create your views here.
class PhotoListView(ListView):
    model = Photo
    template_name = 'photos/index.html'
    context_object_name = 'photos'
    paginate_by = 12

    def get_queryset(self):
        return Photo.objects.filter(is_private=False).select_related('author', 'album')


class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photos/photo_detail.html'
    context_object_name = 'photo'


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['image', 'caption', 'album', 'is_private']
    template_name = 'photos/photo_create.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['album'].qeryset = Album.objects.filter(author=self.request.user)
        return form

    def form_valid(self, form):
        form.instanse.author = self.request.user
        if form.instance.album and form.instance.album.is_private:
            form.instance.is_private = True
            return super().form_valid(form)


class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    fields = ['image', 'caption', 'album', 'is_private']
    template_name = 'photos/photo_create.html'

    def get_queryset(self):
        return Photo.objects.filter(album=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['album'].qyeryset = Album.objects.filter(author=self.request.user)
        return form

    def form_valid(self, form):
        if form.instance.album and form.instance.album.is_private:
            form.instance.is_private = True
        return super().form_valid(form)


class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    template_name = 'photos/photo_confirm_delete.html'
    success_url = reverse_lazy('photos:index')

    def get_queryset(self):
        return Photo.objects.filter(author=self.request.user)


class AlbumDetailView(DetailView):
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


class AlbumUpdateView(LoginRequiredMixin, UpdateView):
    model = Album
    fields = ['title', 'description', 'is_private']
    template_name = 'photos/album_create.html'

    def get_queryset(self):
        return Album.objects.filter(author=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance.is_private:
            form.instance.photos.update(is_private=True)
        return response


class AlbumDeleteView(LoginRequiredMixin, DeleteView):
    model = Album
    template_name = 'photos/album_confirm_delete.html'
    success_url = reverse_lazy('photos:index')

    def get_queryset(self):
        return Album.objects.filter(author=self.request.user)