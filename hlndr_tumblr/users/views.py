#Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, loader, RequestContext
from django.utils import timezone
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# from users.models import User
from users.forms import RegisterForm, LoginForm, ImageForm, ProfileForm, PasswordForm
from users.models import UserProfile

from utils.shortcuts import *

from blog.models import Blog
from following.models import Category
from favorites.models import FaveList

# display profile page
def profile(request, username):
    user = get_object_or_404(User,username=username)
    userprofile = get_object_or_404(UserProfile,user=user)
    return render_to_response('users/profile.html', {'user':user, 'userprofile':userprofile, 'request':request}, context_instance=RequestContext(request))

# display edit profile page and form
@login_required(login_url='/login/')
def edit_profile(request):
	if request.method == 'POST':
		# Get form type by submit request
		edit_action = request.POST['edit_action']
		if edit_action == "avatar":
			forms = ImageForm(request.POST, request.FILES)
		elif edit_action == "profile":
			forms = ProfileForm(request.POST)
		elif edit_action == "password":
			forms = PasswordForm(request.POST)
		else:
			return HttpResponseRedirect("/editprofile/")
		
		# Validate form
		if forms.is_valid():
			
			if edit_action == "avatar":
				file = request.FILES['image']
				#we may want to add an id field here to prevent user from accidently overriding
				filePath = "%s/ProfilePhoto/%s" % (request.user.username, file.name)
				s3_thread(file, filePath)
				request.user.userprofile.avatar = amazon_url + filePath
				request.user.userprofile.save()
				userName = request.user.username
				return HttpResponseRedirect("/%s/profile/" % userName)
			
			if edit_action == "profile":
				blogname = forms.cleaned_data['blogname']
				nickname = forms.cleaned_data['nickname']
				email = forms.cleaned_data['email']
				interests = forms.cleaned_data['interests']

				# save blog
				user_blog = Blog.objects.get(author=request.user)
				user_blog.title = blogname if blogname != user_blog.title else user_blog.title
				user_blog.save()
				
				# save user information
				user = request.user
				user.email = email if user.email != email else user.email
				user.save()

				# save profile information
				userprofile = request.user.userprofile
				userprofile.nickname = nickname if userprofile.nickname != nickname else userprofile.nickname
				userprofile.interests = interests if userprofile.interests != interests else userprofile.interests
				userprofile.save()
				
				return HttpResponseRedirect('/dashboard/')

			if edit_action == "password":
				return save_password_form(request, forms)
					
	imageform = ImageForm()
	profileform = ProfileForm()
	passwordform = PasswordForm()

	blog = Blog.objects.get(author=request.user)

	return render_to_response("users/editprofile.html",
							  {'user':request.user, 'blog':blog,
							  'imageform':imageform,'profileform':profileform,'passwordform':passwordform},
							  context_instance=RequestContext(request))

def save_password_form(request, form):
	password1 = form.cleaned_data['password1']
	password2 = form.cleaned_data['password2']

	if password1 != password2:	
		password_message = "Password mismatch"
	else:
		password_message = "Password Changed Successfully"
		request.user.set_password(password1)
		request.user.save()

	return render_to_response("users/editprofile.html",
							  {'user':request.user, 'imageform':ImageForm(), 
							   'profileform':ProfileForm(), 'passwordform':PasswordForm(), 'password_message':password_message},
							  context_instance=RequestContext(request))

# display list of friends page
@login_required(login_url='/friends/')
def friends(request):
	return render_to_response('users/friends.html',
							  {'users':request.user},
							  context_instance=RequestContext(request))

# login page
def log_in(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('/dashboard/')
				else:
					return render_to_response('users/login.html',
											  {'form':form,
											   'invalid':"Account disabled"},
											  context_instace=RequestContext(request))
			else:
				return render_to_response('users/login.html',
										  {'form':form,
										   'invalid':"Invalid username or password"},
										  context_instance=RequestContext(request))

	template = loader.get_template('users/login.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))

@login_required(login_url='/login/')
def log_out(request):
	logout(request)
	return HttpResponseRedirect('/')

# registration page
def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			
			# Validate fields
			if form.cleaned_data['password1'] == form.cleaned_data['password2']:
				password = form.cleaned_data['password1']
			else:
				return render_to_response('users/register.html',
										  {'form':form,
										   'invalid':"Passwords mismatched"},
										   context_instance=RequestContext(request))
			
			# Django User Data
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
		
			# Validate unique user	
			if User.objects.filter(username=username).count() == 1:
				return render_to_response('users/register.html',
				     					  {'form':form,
						    			   'invalid':"User already exists"},
							    		   context_instance=RequestContext(request))
			# User Profile Data
			birthday = form.cleaned_data['birthday']
			nickname = form.cleaned_data['nickname']
			gender = form.cleaned_data['gender']
			interests = form.cleaned_data['interests']
			
			# Save User to database
			newuser = User(username=username,email=email)
			newuser.set_password(password)
			newuser.save()
			
			# save user profile to database
			user = User.objects.get(username=username)
			newUserProfile = UserProfile.objects.create(user=user,
														birthday=birthday,
														nickname=nickname,
														gender=gender,
														interests=interests)
			
			# Create user's blog information
			Blog.objects.create(author=user)
			# Create user's following information
			Category.objects.create(name="Uncategorized", owner=user.userprofile)
			# Create user's favelist
			FaveList.objects.create(user=user)
	
			return HttpResponseRedirect('/login/')
		else:
			return render_to_response('users/register.html',
									  {'form':form,
									   'invalid':"Some required fields have not been filled"},
									  context_instance=RequestContext(request))
	else:
		form = RegisterForm()

	return render_to_response('users/register.html',
							  context_instance=RequestContext(request))	
