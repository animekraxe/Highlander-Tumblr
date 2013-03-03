# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, loader, RequestContext
from django.utils import timezone
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

#from users.forms import RegisterForm, LoginForm, ImageForm
from friends.models import Friendship, FriendRequest

from utils.shortcuts import *

#function to fill friends page up with desired content
@login_required(login_url='/login/')
def friend_page(request):
	# Get friend request action values
	if request.method == 'POST':
		if 'friend_request_action' in request.POST:
			action_val = request.POST['friend_request_action'].split('_')
			action = action_val[0]
			id = action_val[1]
			friend_request = get_object_or_404(FriendRequest,id=id)
			if action == "accept":
				friend_request.accept()
			if action == "delete":
				friend_request.delete()

	#get the user object from db but 404 if not there
	user = request.user
	
	#get list of friends listed under the user
	friends = [friendship.to_friend for friendship in user.from_friend_set.all()]

	#get list of friends request issued by user
	fr_outgoing = user.invite_sender.all()

	#get list of friend request incoming to user
	fr_incoming = user.invite_reciever.all()

	#list of friends that should be shown (currently lists by recently added friends) [decending]
	#recently_added_friends = [fs.to_friend for fs in user.from_friend_set.order_by('-friendSince')]	

	variables = RequestContext(request, {
		'user': user,
		'friends': friends,
		'incoming_requests':fr_incoming,
		'outgoing_requests':fr_outgoing,
		})

	return render_to_response('friends/friends_page.html', variables)

#function to actually add friends (should be a GET request)
@login_required(login_url='/login/')
def friend_add(request, friendname):
	#make sure the user is authenticated before performing action
	if request.user.is_authenticated(): 
		user = request.user
	else:
		raise Http404
	
	#assuming there is a way to retrieve someones user info
	#it might be a button called "add friend" that issues a
		
	#get the desired friends username
	friend = get_object_or_404(User, username=friendname)
	
	#make sure there was a friend request object
	fr = FriendRequest.objects.filter(sender=friend, reciever=user)
	if fr.count() == 0:
		raise Http404
	else: 
		fr[0].accept();
		return HttpResponseRedirect('/friends/')

	
@login_required(login_url='/login/')
def send_friend_request(request, friendname):
	#make sure the user is authenticated before performing action
	if request.user.is_authenticated(): 
		user = request.user
	else:
		raise Http404

	friend = get_object_or_404(User, username=friendname)

	friendRequest = FriendRequest(sender=user, reciever=friend)
	friendRequest.save()

	# notify recipient of friend request
	notify_user(friend, "Pending Friend Request from %s" % friend.username, "/friends/")

	#not sure if stay on same page or redirect
	return HttpResponseRedirect('/%s/' % friendname)
