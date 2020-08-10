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
from rssapp.api.user import create as user_create, read as user_read, update as user_update, delete as user_delete
from rssapp.api.category import create as category_create, read as category_read, update as category_update, delete as category_delete
from rssapp.api.channel import create as channel_create, read as channel_read, update as channel_update, delete as channel_delete
from rssapp.api.channel import  get_channel_users, get_rsschannel_data
from rssapp.api.adminpanel import get_all

urlpatterns = [
    path('', index_view, name="index"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('admin/', admin_view, name="admin"),
    #api
    path('api/user/create/', user_create, name="user_create"),
    path('api/user/read/', user_read, name="user_read"),
    path('api/user/update/', user_update, name="user_update"),
    path('api/user/delete/', user_delete, name="user_delete"),

    path('api/category/create/', category_create, name="category_create"),
    path('api/category/read/', category_read, name="category_read"),
    path('api/category/update/', category_update, name="category_update"),
    path('api/category/delete/', category_delete, name="category_delete"),

    path('api/channel/create/', channel_create, name="channel_create"),
    path('api/channel/read/', channel_read, name="channel_read"),
    path('api/channel/update/', channel_update, name="channel_update"),
    path('api/channel/delete/', channel_delete, name="channel_delete"),

    path('api/admin/all/', get_all, name="admin_all"),
    path('api/rss/channels/users/', get_channel_users, name="channels_users"),
    path('api/rss/channels/datasource/', get_rsschannel_data, name="rss_datasourse")
]