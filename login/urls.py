from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name="login/password_reset.html"
        ),
        name='reset_password'
    ),
    path(
        'password_reset/done',
        auth_views.PasswordResetDoneView.as_view(
            template_name="login/password_reset_sent.html"
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="login/password_reset_form.html"
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done',
        auth_views.PasswordResetCompleteView.as_view(
            template_name="login/password_reset_done.html"
        ),
        name='password_reset_complete'
    ),
]
