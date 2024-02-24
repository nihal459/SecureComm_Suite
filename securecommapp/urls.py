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
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),
    path('verify_user/<int:pk>/', views.verify_user, name='verify_user'),
    path('view_text_msg/<int:pk>/', views.view_text_msg, name='view_text_msg'),
    path('view_texts', views.view_texts, name='view_texts'),
    path('mark_read/<int:pk>/', views.mark_read, name='mark_read'),
    path('delete_file/<int:pk>/', views.delete_file, name='delete_file'),
    path('file_enc', views.file_enc, name='file_enc'),
    path('image_enc', views.image_enc, name='image_enc'),
    path('delete_image/<int:pk>/', views.delete_image, name='delete_image'),
    path('delete_text/<int:pk>/', views.delete_text, name='delete_text'),
    path('view_files', views.view_files, name='view_files'),
    path('view_file_msg/<int:pk>/', views.view_file_msg, name='view_file_msg'),

    path('serve_file/<path:file_path>/', views.serve_file, name='serve_file'),
    path('mark_read2/<int:pk>/', views.mark_read2, name='mark_read2'),
    path('view_images', views.view_images, name='view_images'),
    path('view_image_msg/<int:pk>/', views.view_image_msg, name='view_image_msg'),

    path('mark_read3/<int:pk>/', views.mark_read3, name='mark_read3'),


    
]