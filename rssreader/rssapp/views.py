from django.shortcuts import render
import requests
from django.http import HttpResponsePermanentRedirect
from rssapp.models import Users

def index_view(request, *args, **kwargs):
    if not request.session.get('userauthenticated'):
        return HttpResponsePermanentRedirect("/login/")
    
    ctx = {"name":request.session['name'], "user_id":request.session['user_id']}
    
    return render(request, "index.html", ctx)

def admin_view(request, *args, **kwargs):
    if not request.session.get('userauthenticated'):
        return HttpResponsePermanentRedirect("/login/")
    
    ctx = {"name":request.session['name'], "user_id":request.session['user_id']}
    
    return render(request, "admin.html", ctx)

def login_view(request, *args, **kwargs):
    ctx = {}
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = Users.objects.filter(username=username, password=password).first()

    if user:
        request.session['user_id'] = user.id
        request.session['userauthenticated'] = user.username
        request.session['name'] = user.name
    else:
        return render(request, "login.html", {"error":"Access denegated, please check your credentials"})
    
    if user.is_admin:
        return HttpResponsePermanentRedirect("/admin/")
    
    return HttpResponsePermanentRedirect("/")

def logout_view(request, *args, **kwargs):
    del request.session['userauthenticated']
    
    return render(request, "login.html", {})