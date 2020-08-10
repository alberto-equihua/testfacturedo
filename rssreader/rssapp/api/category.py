from rest_framework.response import Response
from django.core import serializers
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
from datetime import date
from django.http import HttpResponse, JsonResponse
from rssapp.models import Category
from rssapp.serializers import CategorySerializer

@api_view(['GET', 'POST'])
def create(request):
    category = serializer = None

    try:
        category = Category.objects.create(
            name = request.data.get('name')
        )
        serializer = CategorySerializer(category)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':'Internal server error'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def read(request):
    category = serializer = None

    try:
        category = Category.objects.filter(id=request.data.get('category_id')).first()

        if category:
            serializer = CategorySerializer(category)
        else:
            return JsonResponse({'error':'Category not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':'Internal server error'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def update(request):
    category = serializer = None
    
    try:
        category = Category.objects.filter(id=request.data.get('category_id')).first()

        if category:
            category.name = request.data.get('name')
            category.save()
            serializer = CategorySerializer(category)
        else:
            return JsonResponse({'error':'Category not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':'Internal server error'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def delete(request):
    category = serializer = None
        
    try:
        category = Category.objects.filter(id=request.data.get('category_id')).first()

        if category:
            category.delete()
        else:
            return JsonResponse({'error':'Category not found'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        
        return JsonResponse({'data':'The record has been deleted'}, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JsonResponse({'error':'Internal server error'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
