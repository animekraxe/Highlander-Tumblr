from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response

from utils.shortcuts import *
import random

def home(request):
	posts = []
	recommended_enable = False
	if request.user.is_authenticated():
		recommended_enable = True

	if request.method == 'POST' and 'home_action' in request.POST:
		action = request.POST['home_action']
		if action == 'recommended': 
			posts = rank_blogs(request.user)
			
		elif action == 'random':
			for user in User.objects.all():
				posts += get_user_posts(user)
	
			random.shuffle(posts)
			posts = posts[:30]
	else:
		for user in User.objects.all():
			posts += get_user_posts(user)
	
		random.shuffle(posts)
		posts = posts[:30]
	
	posts = filter_posts_by_privacy(request.user, posts)

	return render_to_response('hlndr_tumblr/homepage.html',
							  {'posts':posts, 'recommended_enable':recommended_enable},
							  context_instance=RequestContext(request))	
