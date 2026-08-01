from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from accounts.forms import RegisterForm


# Create your views here.
class RegisterView(CreateView):
    model = get_user_model()
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.object.pk})


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        is_owner = profile_user == self.request.user

        context['albums'] = profile_user.albums.filter(is_private=False)
        context['photos'] = profile_user.photos.filter(is_private=False, album__isnull=True)

        if is_owner:
            context['private_albums'] = profile_user.albums.filter(is_private=True)
            context['private_photos'] = profile_user.photos.filter(is_private=True, album__isnull=True)

        context['is_owner'] = is_owner
        return context