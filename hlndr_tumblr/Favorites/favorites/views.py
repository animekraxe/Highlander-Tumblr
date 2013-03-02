# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from blog.models import *
from utils.shortcuts import *

import threading

@login_required(login_url='/login/')
def favorites( request ):
    if request.user.is_authenticated():
        user = request.user.username
    favorites = user.userprofile.favorites.all()
    posts = []
    posts = favorites.get_favorites()
    posts = sort_posts_by_newest(posts)
    return render_to_response('favorites/favorites.html', {'posts':posts}, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def add_favorite( request, post_type, postid):
    if request.user.is_authenticated():
        user = request.user.username
    favorites = user.userprofile.favorites.all()
    favorites.add(post_type, postid)
    posts = []
    posts = favorites.get_favorites()
    posts = sort_posts_by_newest(posts)
    return render_to_response('favorites/favorites.html', {'posts':posts}, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def delete_favorite( request, post_type, postid):
    if request.user.is_authenticated():
        user = request.user.username
    favorites = user.userprofile.favorites.all()
    favorites.delete(post_type, postid)
    return HttpResponseRedirect('/' + user.username + '/favorites/')