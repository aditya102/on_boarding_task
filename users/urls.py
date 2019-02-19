from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path

from users import views as user_view

from .forms import CustomPasswordReset

urlpatterns = [
    path('', user_view.register, name="register"),
    path('register/', user_view.register, name="register"),
    path('home/', user_view.home, name="home"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='users/register/password_reset.html',
        form_class=CustomPasswordReset),
        name="password_reset"
    ),
    path('reset_password/done', auth_views.PasswordResetDoneView.as_view(
        template_name='users/register/password_reset_done.html'),
        name="password_reset_done"
    ),
    path('reset_password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/register/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path('reset_password/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/register/password_reset_complete.html'),
        name='password_reset_complete'
    ),
    url('activate/(?P<uidb64>[0-9A-Za-z\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        user_view.activate, name='activate'
    ),
]
