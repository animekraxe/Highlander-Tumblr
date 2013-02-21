# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from forms import *
from models import Message 

# View all messages in descending order.
# Set messages to not new 
@login_required(login_url='/login/')
def inbox(request):

	message_list = Message.objects.filter(recipient=request.user).order_by('-send_date')

	for message in message_list:
		message.is_new = False
		message.save()
	
	return render_to_response('messages/inbox.html',
							  {'user':request.user, 'message_list':message_list},
							  context_instance=RequestContext(request))

# helper for rendering compose message page
def _render_compose(request, form, invalid):
	return render_to_response('messages/compose.html',
							  {'form':form, 'invalid':invalid},
							   context_instance=RequestContext(request))

# compose new message page
@login_required(login_url='/login/')
def compose(request):
	if request.method == 'POST':
		form = ComposeMessageForm(request.POST)
		if form.is_valid():
			recipient = form.cleaned_data['recipient']

			if User.objects.filter(username=recipient).count() == 0:
				return _render_compose(request, form, "User does not exist")
			
			recipient = User.objects.get(username=recipient)
			title = form.cleaned_data['title']
			message = form.cleaned_data['message']

			Message.objects.create(sender=request.user,
								   recipient=recipient,
								   title=title,
								   message=message)

			return HttpResponseRedirect('/dashboard/')
		else:
			return _render_compose(request, form, "No text in message")
	else:
		form = ComposeMessageForm()

	return _render_compose(request, form, "")

