#Create your views here.
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from utils.shortcuts import *
from dashboard.models import Notification

@login_required(login_url='/login/')
def dashboard(request):
	if request.user.is_authenticated():
		user = request.user

	posts = get_followed_posts(request.user) + get_user_posts(request.user) + get_friend_posts(request.user)
	posts = filter_posts_by_privacy(user, posts)
	posts = list(set(posts))	
	if request.method == 'POST':
		if 'searchbar' in request.POST:
			posts = sort_posts_by_searchbar(posts, request)
		if 'delete_notification' in request.POST:
			notification_id = int(request.POST['delete_notification'])
			notification = Notification.objects.get(id=notification_id)
			link = notification.link
			notification.delete()
			return HttpResponseRedirect(link)
	else:
		posts = sort_posts_by_newest(posts)

	recommendations = rank_blogs(request.user)

	return render_to_response('dashboard/dashboard.html',
							  {'posts':posts, 'recommendations':recommendations}, 
							  context_instance=RequestContext(request))

@login_required(login_url='/login/')
def deletepost(request, post_type, post_id):
	posts = get_user_posts(request.user)
	for post in posts:
		if post.classname().lower() == post_type:
			if post.id == int(post_id):
				delete_post(post)
				return HttpResponseRedirect('/' + request.user.username + '/posts/')
	raise Http404

@login_required(login_url='/login/')
def viewposts(request, username):
	posts = get_user_posts(request.user)
	if request.method == 'POST':
		query = request.POST['searchbar']
		if query == 'newest':
			posts = sort_posts_by_newest(posts)
		elif query == 'oldest':
			posts = sort_posts_by_oldest(posts)
		elif query == 'search':
			# Implement search by tags here
			tags = request.POST['searchbox']
			taglist = get_tag_list(tags)

			posts = []
			for tag in taglist:
				posts += get_user_posts_by_tag(request.user,tag)	
		else:
			posts = sort_posts_by_newest(posts)
	else:
		posts = sort_posts_by_newest(posts)
	
	return render_to_response('dashboard/viewposts.html',
							  {'posts':posts, 'user':request.user},
							  context_instance=RequestContext(request))			
