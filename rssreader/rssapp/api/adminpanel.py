from rest_framework.response import Response
from django.core import serializers
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
from datetime import date
from django.http import HttpResponse, JsonResponse
from rssapp.models import Users, RssChannel, Category, Feed, Entry
from rssapp.serializers import UsersSerializer, CategorySerializer, RssChannelSerializer

@api_view(['GET', 'POST'])
def get_all(request):
    user = category = rsschanel = serializer = None
    data = {}

    try:
        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        data['users'] = serializer.data

        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        data['categories'] = serializer.data

        channels = RssChannel.objects.all()
        serializer = RssChannelSerializer(channels, many=True)
        data['channels'] = serializer.data

        rsschanel = RssChannel.objects.all()
        return JsonResponse({'data':data}, safe=False, status=status.HTTP_200_OK)
    
    except Exception as e:
        return JsonResponse({'error':'Internal server error'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)