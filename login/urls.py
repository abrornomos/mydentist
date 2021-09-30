from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    # path('password_change/', views.register, name='register'),
    # path('password_change/done', views.sign_in, name='login'),
    # path('password_reset/', views.sign_out, name='logout'),
    # path('password_reset/done', views.register, name='register'),
    # path('reset/<uidb64>/<token>', views.sign_in, name='login'),
    # path('reset/done', views.sign_out, name='logout'),
]
