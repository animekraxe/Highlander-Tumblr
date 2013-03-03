# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from blog.models import *
from utils.shortcuts import *

@login_required(login_url='/login/')
def favorites( request ):
	if request.user.is_authenticated():
		user = request.user
		favorites = user.favelist.get_favorites()
	
	if request.method == 'POST':
		if 'favelist_action' in request.POST:	
			post_values = request.POST['favelist_action'].split('_')
			post_type = post_values[0]
			post_id = int(post_values[1])
			exec "post = %s.objects.get(id=%d)" % (post_type, post_id)	
			request.user.favelist.delete(post)

		if 'searchbar' in request.POST:
			favorites = sort_posts_by_searchbar(favorites, request)
	else:
		favorites = sort_posts_by_newest(favorites)
	return render_to_response('favorites/favorites.html', {'favorites':favorites}, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def add_favorite( request, post_type, postid):
    if request.user.is_authenticated():
        user = request.user
    favorites = user.userprofile.favorites.all()
    favorites.add(post_type, postid)
    posts = []
    posts = favorites.get_favorites()
    posts = sort_posts_by_newest(posts)
    return render_to_response('favorites/favorites.html', {'posts':posts}, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def delete_favorite( request, post_type, postid):
    if request.user.is_authenticated():
        user = request.user
    favorites = user.userprofile.favorites.all()
    favorites.delete(post_type, postid)
    return HttpResponseRedirect('/' + user.username + '/favorites/')
