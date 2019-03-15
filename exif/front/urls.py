from django.contrib import admin
from django.urls import path, include

## this is for development image hosting
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

from . import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload2, name='upload'),
    path('img/<str:user>/<str:filename>', views.imageView),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', views.signout, name='logout'),
    path('register', views.register, name='register'),
    path('admin', views.admin, name='admin'),
    path('profile', views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
