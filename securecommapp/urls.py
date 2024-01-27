from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('user_register', views.user_register, name='user_register'),
    path('user_login', views.user_login, name='user_login'),
    path('user_home', views.user_home, name='user_home'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admins_home', views.admins_home, name='admins_home'),
    path('SignOut', views.SignOut, name='SignOut'),
    path('text_enc', views.text_enc, name='text_enc'),
    path('manage_users', views.manage_users, name='manage_users'),


    
]