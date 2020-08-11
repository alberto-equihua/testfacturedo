from rest_framework.response import Response
from django.core import serializers
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
from datetime import date
from django.http import HttpResponse, JsonResponse
from rssapp.models import Users
from rssapp.serializers import UsersSerializer

@api_view(['GET', 'POST'])
def create(request):
    user = serializer = None

    try:
        user = Users.objects.create(
            name = request.data.get('name'),
            username = request.data.get('username'),
            password = request.data.get('password'),
            is_admin = request.data.get('is_admin')
        )

        serializer = UsersSerializer(user)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':'Internal server error'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def read(request):
    user = serializer = None

    try:
        if request.data.get('user_id'):
            user = Users.objects.filter(id=request.data.get('user_id')).first()
        else:
            user = Users.objects.all()
            serializer = UsersSerializer(user, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

        if user:
            serializer = UsersSerializer(user)
        else:
            return JsonResponse({'error': 'User not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':'Internal server error'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def update(request):
    user = serializer = None

    try:
        user = Users.objects.filter(id=request.data.get('user_id')).first()
        
        if user:
            user.name = request.data.get('name')
            user.username = request.data.get('username')
            user.password = request.data.get('password')
            user.is_admin = request.data.get('is_admin')
            user.save()
            serializer = UsersSerializer(user)
        else:
            return JsonResponse({'error': 'User not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':'Internal server error'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def delete(request):
    user = serializer = None
        
    try:
        user = Users.objects.filter(id=request.data.get('user_id')).first()
        
        if user:
            user.delete()
        else:
            return JsonResponse({'data': 'User not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        
        return JsonResponse({'data': 'The User has been deleted'}, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':'Internal server error'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)