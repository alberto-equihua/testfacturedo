"""rssreader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rssapp.views import index_view, login_view, logout_view, admin_view
from rssapp.api import create, read, update, delete, gel_all, get_rsschannel_data, get_channel_users

urlpatterns = [
    path('', index_view, name="index"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('admin/', admin_view, name="admin"),
    path('api/crud/create/', create, name="create"),
    path('api/crud/read/', read, name="read"),
    path('api/crud/update/', update, name="update"),
    path('api/crud/delete/', delete, name="delete"),
    path('api/crud/all/', gel_all, name="all"),
    path('api/rss/chanles/datasource/', get_rsschannel_data, name="rssdatasourse"),
    path('api/rss/chanles/users/', get_channel_users, name="channelsusers")
]