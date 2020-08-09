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
from rssapp.rss import RssChannelData

request_values = [
    'model', 'name', 'username', 'passwor', 'is_admin', 'res_id', 'category_id'
]

@api_view(['POST'])
def create(request):
    user = category = rsschanel = serializer = None
    model = request.data.get('model', False)

    try:
        if model == 'user':
            user = Users.objects.create(
                name = request.data.get('name'),
                username = request.data.get('username'),
                password = request.data.get('password'),
                is_admin = request.data.get('is_admin')
            )
            serializer = UsersSerializer(user)
        elif model == 'category':
            category = Category.objects.create(
                name = request.data.get('name')
            )
            serializer = CategorySerializer(category)
        elif model == 'channel':
            category_id = Category.objects.filter(id=request.data.get('category_id')).first()
            
            if not category_id:
                return JsonResponse({'error':'Id Category not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
            
            rsschanel = RssChannel.objects.create(
                name = request.data.get('name'),
                url = request.data.get('url'),
                category_id = category_id,
            )
            serializer = RssChannelSerializer(rsschanel)
        else:
            return JsonResponse({'error':'Model not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':'Internal server error'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def read(request):
    user = category = rsschanel = serializer = None
    model = request.data.get('model', False)

    try:
        if model == 'user':
            if request.data.get('res_id'):
                user = Users.objects.filter(id=request.data.get('res_id')).first()
            else:
                user = Users.objects.all()
                serializer = UsersSerializer(user, many=True)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

            if user:
                serializer = UsersSerializer(user)
            else:
                return JsonResponse({'error':'User not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        elif model == 'category':
            category = Category.objects.filter(id=request.data.get('res_id')).first()

            if category:
                serializer = CategorySerializer(category)
            else:
                return JsonResponse({'error':'Category not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        elif model == 'channel':
            if request.data.get('res_id'):
                rsschanel = RssChannel.objects.filter(id=request.data.get('res_id')).first()
            else:
                rsschanel = RssChannel.objects.all()
                serializer = RssChannelSerializer(rsschanel, many=True)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
            if rsschanel:
                serializer = RssChannelSerializer(rsschanel)
            else:
                return JsonResponse({'error':'Channel not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'error':'Model not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':'Internal server error'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def update(request):
    user = category = rsschanel = serializer = None
    model = request.data.get('model', False)
    
    try:
        if model == 'user':
            user = Users.objects.filter(id=request.data.get('res_id')).first()
            
            if user:
                user.name = request.data.get('name')
                user.username = request.data.get('username')
                user.password = request.data.get('password')
                user.is_admin = request.data.get('is_admin')
                user.save()
                serializer = UsersSerializer(user)
            else:
                return JsonResponse({'error':'User not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        elif model == 'category':
            category = Category.objects.filter(id=request.data.get('res_id')).first()

            if category:
                category.name = request.data.get('name')
                category.save()
                serializer = CategorySerializer(category)
            else:
                return JsonResponse({'error':'Category not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        elif model == 'channel':
            
            rsschanel = RssChannel.objects.filter(id=request.data.get('res_id')).first()

            if request.data.get('addchannel') and request.data.get('user_id') and request.data.get('channel_id'):
                user = Users.objects.filter(id=request.data.get('user_id')).first()
                rsschanel = RssChannel.objects.filter(id=request.data.get('channel_id')).first()

                if user and rsschanel:
                    user.channels_ids.add(rsschanel)
                    return JsonResponse({'data':'Channel added'}, safe=False, status=status.HTTP_200_OK)

            category_id = Category.objects.filter(id=request.data.get('category_id')).first()
            
            if not category_id:
                return JsonResponse({'error':'Id Category not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
            
            if rsschanel:
                rsschanel.name = request.data.get('name')
                rsschanel.url = request.data.get('url')
                rsschanel.category_id = category_id
                rsschanel.save()
                serializer = RssChannelSerializer(rsschanel)
            else:
                return JsonResponse({'error':'Channel not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'error':'Model not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JsonResponse({'error':'Internal server error'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def delete(request):
    user = category = rsschanel = serializer = None
    model = request.data.get('model', False)
        
    try:
        if model == 'user':
            user = Users.objects.filter(id=request.data.get('res_id')).first()
            
            if user:
                user.delete()
            else:
                return JsonResponse({'error':'User not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        elif model == 'category':
            category = Category.objects.filter(id=request.data.get('res_id')).first()

            if category:
                category.delete()
            else:
                return JsonResponse({'error':'Category not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        elif model == 'channel':
            rsschanel = RssChannel.objects.filter(id=request.data.get('res_id')).first()

            if request.data.get('deletechannel') and request.data.get('channel_id') and request.data.get('user_id'):
                user = Users.objects.filter(id=request.data.get('user_id')).first()
                rsschanel = RssChannel.objects.filter(id=request.data.get('channel_id')).first()

                if user and rsschanel:
                    user.channels_ids.remove(rsschanel)
                    return JsonResponse({'data':'Channel has been deleted'}, safe=False, status=status.HTTP_200_OK)

            if rsschanel:
                rsschanel.delete()
            else:
                return JsonResponse({'error':'Channel not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'error':'Model not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'data':'The record has been deleted'}, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JsonResponse({'error':'Internal server error'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def gel_all(request):
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

@api_view(['POST', 'GET'])
def get_channel_users(request):
    channels = []
    channels_ids = channels_exclude_ids = serializer = None
    user_id = request.data.get('user_id', False)

    if user_id:
        user = Users.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({'error':'User not found'}, safe=False, status=status.HTTP_200_OK)  
        
        cursor = connection.cursor()
        cursor.execute("""
            SELECT ch.id, ch.name, ch.url, true 'added'
            from rssapp_rsschannel ch INNER JOIN rssapp_users_channels_ids uch
            ON uch.rsschannel_id = ch.id 
            where uch.users_id = %s
            union
            SELECT ch.id, ch.name, ch.url, false 'added' 
            FROM rssapp_rsschannel ch 
            where ch.id not in (SELECT rsschannel_id from rssapp_users_channels_ids  where users_id = %s)
        """, [user_id, user_id])

        for row in cursor.fetchall():
            channels.append({'id':row[0], 'name': row[1], 'url': row[2], 'added':row[3]})

        return JsonResponse({'data':channels}, safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error':'User not found'}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET','POST'])
def get_rsschannel_data(request):
    channels = user = rss = serializer = None
    feeds = entries = {}, []
    user_id = 0

    try:
        if request.method == 'GET':
            channels = RssChannel.objects.all()
            serializer = RssChannelSerializer(channels, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            user_id = request.data.get('user_id', False)

            if user_id:
                user = Users.objects.filter(id=user_id).first()
                if user:
                    rss = RssChannelData()

                    for ch in user.channels_ids:
                        feed, entries = rss.get_data(ch.url)
                        if len(feed) > 0 and len(entries) > 0:
                            print(feed)
                serializer = RssChannelSerializer(channels, many=True)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
                
    except Exception as e:
        print(e)
        return JsonResponse({'error':'Internal server error'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)