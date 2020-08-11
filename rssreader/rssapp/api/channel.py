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

@api_view(['GET', 'POST'])
def create(request):
    rsschanel = serializer = None

    try:
        category_id = Category.objects.filter(id=request.data.get('category_id')).first()
        
        if not category_id:
            return JsonResponse({'error':'Id Category not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        
        rsschanel = RssChannel.objects.create(
            name = request.data.get('name'),
            url = request.data.get('url'),
            category_id = category_id,
        )
        serializer = RssChannelSerializer(rsschanel)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':'Internal server error'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def read(request):
    rsschanel = serializer = None

    try:
        if request.data.get('res_id'):
            rsschanel = RssChannel.objects.filter(id=request.data.get('channel_id')).first()
        else:
            rsschanel = RssChannel.objects.all()
            serializer = RssChannelSerializer(rsschanel, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        if rsschanel:
            serializer = RssChannelSerializer(rsschanel)
        else:
            return JsonResponse({'error':'Channel not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return JsonResponse({'error':'Internal server error'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def update(request):
    rsschanel = serializer = None
    
    try:
        rsschanel = RssChannel.objects.filter(id=request.data.get('channel_id')).first()

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

        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':'Internal server error'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def delete(request):
    rsschannel = serializer = None

    try:
        if request.data.get('channel_id') and request.data.get('user_id'):
            user = Users.objects.filter(id=request.data.get('user_id')).first()
            rsschannel = RssChannel.objects.filter(id=request.data.get('channel_id')).first()

            if user and rsschannel:
                user.channels_ids.remove(rsschannel)
                return JsonResponse({'data':'Channel has been deleted'}, safe=False, status=status.HTTP_200_OK)
        
        rsschannel = RssChannel.objects.filter(id=request.data.get('channel_id')).first()
        
        if rsschannel:
            rsschannel.delete()
        else:
            return JsonResponse({'error':'Channel not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'data':'The record has been deleted'}, safe=False, status=status.HTTP_200_OK)
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
            SELECT ch.id, ch.name, ch.url, cat.name category, true 'added'
            from rssapp_rsschannel ch INNER JOIN rssapp_users_channels_ids uch
            ON uch.rsschannel_id = ch.id INNER JOIN rssapp_category cat
            ON cat.id = ch.category_id_id 
            where uch.users_id = %s
            union
            SELECT ch.id, ch.name, ch.url, cat.name category, false 'added' 
            FROM rssapp_rsschannel ch INNER JOIN rssapp_category cat
            ON cat.id = ch.category_id_id
            where ch.id not in (SELECT rsschannel_id from rssapp_users_channels_ids  where users_id = %s)
        """, [user_id, user_id])

        for row in cursor.fetchall():
            channels.append({'id':row[0], 'name': row[1], 'url': row[2], 'category':row[3], 'added':row[4]})

        return JsonResponse({'data':channels}, safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error':'User not found'}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET','POST'])
def get_rsschannel_data(request):
    channels = []
    user_id = 0
    user = None
    
    try:
        if request.data.get('all'):
            user_id = request.data.get('user_id')
            
            if user_id:
                user = Users.objects.filter(id=user_id).first()
                
                for ch in user.channels_ids.all():
                    channels.append(ch)
                serializer = RssChannelSerializer(channels, many=True)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error':'User not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        elif request.data.get('async'):
            user_id = request.data.get('user_id', False)

            if user_id:
                user = Users.objects.filter(id=user_id).first()
                if user:
                    rss = RssChannelData()

                    for ch in user.channels_ids.all():
                        rss.get_data(ch.url)
                        feed, entries = rss.feed, rss.entries
                        
                        if len(feed) > 0 and len(entries) > 0:
                            f = Feed.objects.create(
                                title = feed['title'], 
                                link = feed['link'], 
                                description = feed['description']
                            )
                            
                            ch.feed_id = f
                            ch.save()
                            
                            for en in entries:
                                e = Entry.objects.create(
                                    entry_id = en['id'],
                                    link = en['link'],
                                    published = en['published'],
                                    summary = en['summary']
                                )
                                ch.entries_ids.add(e)
                            
                            channels.append(ch)

                serializer = RssChannelSerializer(channels, many=True)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
                
    except Exception as e:
        return JsonResponse({'error':'Internal server error'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

