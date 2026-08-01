from accounts.views import RegisterView, ProfileView
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
]