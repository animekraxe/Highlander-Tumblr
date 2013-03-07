# Create your views here
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from blog.constants import *
from blog.models import *
from blog.forms import *
from utils.shortcuts import *

import threading

amazon_url = "https://s3-us-west-1.amazonaws.com/highlander-tumblr-test-bucket/"

def post_page(request, post_type, post_id):
	exec "post = %s.objects.get(id=%d)" % (post_type, int(post_id))

	posts = [post]
	posts = filter_posts_by_privacy(request.user, posts)
	if len(posts) == 0:
		raise Http404
	
	if request.method == 'POST':
		if not request.user.is_authenticated():
			return HttpResponseRedirect('/login/')

		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.cleaned_data['comment']
			exec "Comment.objects.create(comment=comment, user=request.user, %s=post)" % post.classname().lower()
	else:
		form = CommentForm()

	return render_to_response('blog/post.html',
							  {'post':post, 'commentform':form, 'user':request.user},
							  context_instance=RequestContext(request))

def reblog_action(request, username):
	if request.method == 'POST':
		if 'reblog_action' in request.POST:
			values = request.POST['reblog_action'].split('_')
			post_type = values[1]
			post_id = int(values[2])
			exec "post = %s.objects.get(id=%d)" % (post_type, post_id)
			
			form = ReblogForm(request.POST)
			
			if form.is_valid():
				author = request.user
				
				title = form.cleaned_data['title']
				description = form.cleaned_data['description']

				quote = form.cleaned_data['quote']
				source = form.cleaned_data['source']

				link = form.cleaned_data['link']

				tags = form.cleaned_data['tags']
				privacy = form.cleaned_data['privacy']

			newpost = None
			if post.classname() == 'TextPost':
				if description == "":
					return "No text in post"
				newpost = TextPost.objects.create(title=title,
						    					  text=description,
												  privacy=privacy,
												  author=author)
			elif post.classname() == 'QuotePost':
				if quote == "":
					return "No quote in post"
				newpost = QuotePost.objects.create(title=title,
							  	 		   	 	   quote=quote,
										 		   source=source,
										 		   privacy=privacy,
										 		   author=author)
			elif post.classname() == 'LinkPost':
				if link == "":
					return "No link in post"
				newpost = LinkPost.objects.create(title=title,
												  link=link,
												  description=description,
												  privacy=privacy,
												  author=author)
			elif post.classname() == 'ChatPost':
				if description == "":
					return "No chat in post"
				newpost = ChatPost.objects.create(title=title,
												  chat=description,
												  privacy=privacy,
												  author=author)
			elif post.classname() == 'PhotoPost':
				newpost = PhotoPost.objects.create(filename=post.filename,
												   url=post.url,
												   caption=description,
												   privacy=privacy,
												   author=author)
			elif post.classname() == 'AudioPost':
				newpost = AudioPost.objects.create(filename=post.filename,
												   url=post.url,
												   description=description,
												   privacy=privacy,
												   author=author)
			elif post.classname() == 'VideoPost':
				newpost = VideoPost.objects.create(filename=post.filename,
												   url=post.url,
												   description=description,
												   privacy=privacy,
												   author=author)
			else:
				raise Http404

			if newpost is not None:
				save_tags(newpost, tags)
				post.reblogs.add(newpost)
			
			return None

@login_required(login_url='/login/')
def blog_post_action(request, username):
	if request.method == 'POST':
		if request.is_ajax():
			print "THIS IS AJAX"
		else:
			print "THIS IS NOT AJAX"

		post_action_values = request.POST['post_action'].split('_')
		post_action = post_action_values[0]
		post_type = post_action_values[1]
		post_id = int(post_action_values[2])
		exec "post = %s.objects.get(id=%d)" % (post_type, post_id)
		
		if post_action == "like":
			request.user.userprofile.like_post(post)
		if post_action == "favorite":
			request.user.favelist.add(post)
			
	return HttpResponseRedirect('/%s/' % username)

# displays a users blog page if user exists
def blogpage(request,username):
	reblog_error = False
	reblog_message = ""
	if request.method == 'POST':
		reblog_message = reblog_action(request, username)
		if reblog_message is not None:
			reblog_error = True

	author = get_object_or_404(User,username=username)
	blog = get_object_or_404(Blog, author=author)

	is_friend = False
	if request.user.is_authenticated():
		if author.from_friend_set.filter(to_friend=request.user).count() == 1:
			is_friend = True

	posts = get_user_posts(author)
	posts = filter_posts_by_privacy(request.user, posts)

	# sort from oldest to newest, then reverse to get latest
	posts = reversed(sorted(posts, key=lambda post: post.post_date))

	reblog_form = ReblogForm()
	
	return render_to_response('blog/blogpage.html',
							  {'author':author, 'posts':posts, 'blog':blog, 'is_friend':is_friend,
							   'reblog_error':reblog_error, 'reblog_error_message':reblog_message, 'reblog_form':reblog_form},
							   context_instance=RequestContext(request))

@login_required(login_url='/login/')
def new_text_post(request):
	invalid = ""
	if request.method == 'POST':
		form = TextForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			text = form.cleaned_data['text']
			privacy = form.cleaned_data['privacy']	
			post = TextPost.objects.create(title=title,
										   text=text,
										   privacy=privacy,
										   author=request.user,)
			tags = form.cleaned_data['tags']
			save_tags(post,tags)

			if int(privacy) in [PRIVACY_ALL, PRIVACY_FRIENDS]:
				notify_users_friends(request.user,
									 "%s made a new text post" % request.user.username, 
									 "/post/%s/%d" % (post.classname(),post.id))
						
			return HttpResponseRedirect('/dashboard/')
		else:
			invalid = "No text in post"
	else:
		form = TextForm()
	
	return render_to_response('blog/textform.html',
							  {'form':form, 'invalid':invalid},
							  context_instance=RequestContext(request))

@login_required(login_url='login')
def new_photo_post(request):
	invalid = ""
	if request.method == 'POST':
		form = PhotoForm(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES['photo']
			caption = form.cleaned_data['caption']
			privacy = form.cleaned_data['privacy']	
			post = PhotoPost.objects.create(filename=file.name,
											url="",
											caption=caption,
											privacy=privacy,
											author=request.user)
			tags = form.cleaned_data['tags']
			save_tags(post,tags)
			
			if int(privacy) in [PRIVACY_ALL, PRIVACY_FRIENDS]:
				notify_users_friends(request.user,
									 "%s made a new photo post" % request.user.username, 
									 "/post/%s/%d" % (post.classname(),post.id))

			filepath = "%s/image/%s/%s" % (request.user.username, str(post.id), file.name)
			s3_thread(file, filepath)
			post.url = amazon_url + filepath
			post.save()
			return HttpResponseRedirect('/dashboard/')
		else:
			invalid = "No Photo Selected"
	else:
		form = PhotoForm()
	return render_to_response('blog/photoform.html',
							  {'form':form, 'invalid':invalid},
							  context_instance=RequestContext(request))

@login_required(login_url='/login/')
def new_video_post(request):
	invalid = ""
	if request.method == 'POST':
		form = VideoForm(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES['video']
			description = form.cleaned_data['description']
			privacy = form.cleaned_data['privacy']	
			post = VideoPost.objects.create(filename=file.name,
										    url="",
											description=description,
											privacy=privacy,
											author=request.user)
			tags = form.cleaned_data['tags']
			save_tags(post,tags)

			if int(privacy) in [PRIVACY_ALL, PRIVACY_FRIENDS]:
				notify_users_friends(request.user,
									 "%s made a new video post" % request.user.username, 
									 "/post/%s/%d" % (post.classname(),post.id))

			filepath = "%s/video/%s/%s" % (request.user.username, str(post.id), file.name)
			s3_thread(file, filepath)
			post.url = amazon_url + filepath
			post.save()
			return HttpResponseRedirect('/dashboard/')
		else:
			invalid = "No Video Selected"
	else:
		form = VideoForm()
	return render_to_response('blog/videoform.html',
							  {'form':form, 'invalid':invalid},
							  context_instance=RequestContext(request))

@login_required(login_url='/login/')
def new_audio_post(request):
	invalid = ""
	if request.method == 'POST':
		form = AudioForm(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES['audio']
			description = form.cleaned_data['description']
			privacy = form.cleaned_data['privacy']	
			post = AudioPost.objects.create(filename=file.name,
										    url="",
											description=description,
											privacy=privacy,
											author=request.user)
			tags = form.cleaned_data['tags']
			save_tags(post,tags)
			
			if int(privacy) in [PRIVACY_ALL, PRIVACY_FRIENDS]:
				notify_users_friends(request.user,
									 "%s made a new audio post" % request.user.username, 
									 "/post/%s/%d" % (post.classname(),post.id))

			filepath = "%s/audio/%s/%s" % (request.user.username, str(post.id), file.name)
			s3_thread(file, filepath)
			post.url = amazon_url + filepath
			post.save()
			return HttpResponseRedirect('/dashboard/')
		else:
			invalid = "No Audio Selected"
	else:
		form = AudioForm()
	return render_to_response('blog/audioform.html',
							  {'form':form, 'invalid':invalid},
							  context_instance=RequestContext(request))

@login_required(login_url='/login/')
def new_quote_post(request):
	invalid = ""
	if request.method == 'POST':
		form = QuoteForm(request.POST)
		if form.is_valid():
			quote = form.cleaned_data['quote']
			source = form.cleaned_data['source']
			privacy = form.cleaned_data['privacy']	
			post = QuotePost.objects.create(quote=quote,
										    source=source,
											privacy=privacy,
											author=request.user)
			tags = form.cleaned_data['tags']
			save_tags(post,tags)
				
			if int(privacy) in [PRIVACY_ALL, PRIVACY_FRIENDS]:
				notify_users_friends(request.user,
									 "%s made a new quote post" % request.user.username, 
									 "/post/%s/%d" % (post.classname(),post.id))

			return HttpResponseRedirect('/dashboard/')
		else:
			invalid = "No quote in post"
	else:
		form = QuoteForm()
	return render_to_response('blog/quoteform.html',
							  {'form':form, 'invalid':invalid},
							  context_instance=RequestContext(request))

@login_required(login_url='/login/')
def new_link_post(request):
	invalid = ""
	if request.method == 'POST':
		form = LinkForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			link = form.cleaned_data['link']
			description = form.cleaned_data['description']
			privacy = form.cleaned_data['privacy']	
			post = LinkPost.objects.create(title=title,
										   link=link,
										   description=description,
										   privacy=privacy,
										   author=request.user)
			tags = form.cleaned_data['tags']
			save_tags(post,tags)
			
			if int(privacy) in [PRIVACY_ALL, PRIVACY_FRIENDS]:
				notify_users_friends(request.user,
									 "%s made a new link post" % request.user.username, 
									 "/post/%s/%d" % (post.classname(),post.id))

			return HttpResponseRedirect('/dashboard/')
		else:
			invalid = "No link in post"
	else:
		form = LinkForm()
	return render_to_response('blog/linkform.html',
							  {'form':form, 'invalid':invalid},
							  context_instance=RequestContext(request))

@login_required(login_url='/login/')
def new_chat_post(request):
	invalid = ""
	if request.method == 'POST':
		form = ChatForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			chat = form.cleaned_data['chat']
			privacy = form.cleaned_data['privacy']	
			post = ChatPost.objects.create(title=title,
										   chat=chat,
										   privacy=privacy,
										   author=request.user)
			tags = form.cleaned_data['tags']
			save_tags(post,tags)
			
			if int(privacy) in [PRIVACY_ALL, PRIVACY_FRIENDS]:
				notify_users_friends(request.user,
									 "%s made a new chat post" % request.user.username, 
									 "/post/%s/%d" % (post.classname(),post.id))

			return HttpResponseRedirect('/dashboard/')
		else:
			invalid = "No chat in post"
	else:
		form = ChatForm()
	return render_to_response('blog/chatform.html',
							  {'form':form, 'invalid':invalid},
							  context_instance=RequestContext(request))

