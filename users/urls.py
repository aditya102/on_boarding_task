from django.contrib.auth import views as auth_views
from django.urls import path

from users import views as user_view

urlpatterns = [
    path('', user_view.register, name="register"),
    path('register/', user_view.register, name="register"),
    path('home/', user_view.home, name="home"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
]
