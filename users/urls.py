
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import change_grasp_power_view
from .views import UserView, signup

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login'), name='logout'),
    path('profile/',  login_required(UserView.as_view()), name='profile'),
    path('signup/', signup, name='signup'),
    path('change_grasp_power/', change_grasp_power_view, name='change_grasp_power'),
]