# Create your views here
from django.http import HttpResponseRedirect, HttpResponse
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

@login_required(login_url='/login/')
def blog_post_action(request, username):
	if request.method == 'POST':
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
	
	return render_to_response('blog/blogpage.html',
							  {'author':author, 'posts':posts, 'blog':blog, 'is_friend':is_friend},
							   context_instance=RequestContext(request))

@login_required(login_url='/login/')
def new_text_post(request):
	invalid = ""
	if request.method == 'POST':
		form = TextForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			slug = slugify(title)
			text = form.cleaned_data['text']
			privacy = form.cleaned_data['privacy']	
			post = TextPost.objects.create(title=title,
										   slug=slug,
										   text=text,
										   privacy=privacy,
										   author=request.user,)
			tags = form.cleaned_data['tags']
			save_tags(post,tags)
						
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

			return HttpResponseRedirect('/dashboard/')
		else:
			invalid = "No chat in post"
	else:
		form = ChatForm()
	return render_to_response('blog/chatform.html',
							  {'form':form, 'invalid':invalid},
							  context_instance=RequestContext(request))

