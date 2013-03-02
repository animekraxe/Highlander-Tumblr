from django.db import models
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from users.models import UserProfile
from following.models import Category
from following.forms import CreateCategoryForm

#searches all categories, deletes otheruser from those categorizes and then adds to category
def addToCategory(user, otheruser, category):
    user_categories = Category.objects.filter(owner=user)
    #searches all categorizes and removes otheruser from that category
    for single_category in user_categories:
        for a_categorized_user in single_category.categorized_users.all():
            if otheruser == a_categorized_user:
                single_category.categorized_users.remove(otheruser)
    #getting specific category, must exist already
    category_to_add_to = Category.objects.get(name=category, owner=user)
    #actual adding to category
    category_to_add_to.categorized_users.add(otheruser)


@login_required(login_url='/login/')
def following(request):
    if request.user.is_authenticated():
        user = request.user

	myself = get_object_or_404(User, username=user.username)
	myprofile = get_object_or_404(UserProfile, user=myself)
	followlist = myprofile.following.all()
	create_message = ""

	if request.method == 'POST':
		form = CreateCategoryForm(request.POST)
		if form.is_valid():
			new_category = form.cleaned_data['new_category']
			if Category.objects.filter(owner=myprofile, name=new_category).count() == 1:
				create_message = "Category Already Exist"
			else:
				create_message = "Category Created Successfully"
				Category.objects.create(owner=myprofile, name=new_category)
		else:
			create_message = "Only Alphanumerics Spaces, and @/./+/- characters allowed"
	else:
		form = CreateCategoryForm()

	temp_categories = list(Category.objects.filter(owner=myprofile))
	temp_categories = sorted(temp_categories, key=lambda category: category.name.lower())
	temp_categories = filter (lambda Category: Category.name != "Uncategorized", temp_categories)
	temp_categories.append(Category.objects.get(owner=myprofile, name="Uncategorized"))
	all_categories = temp_categories

    return render_to_response('following/following.html',
                              {'follower_list':followlist, 'count':followlist.count(),
                              'all_categories':all_categories, 'form':form, 'create_message':create_message},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def follow(request, username):
    if request.user.is_authenticated():
        user = request.user.username
    #following
    myself = get_object_or_404(User, username=request.user.username)
    myprofile = get_object_or_404(UserProfile, user=myself)

    other = get_object_or_404(User, username=username)
    otherprofile = get_object_or_404(UserProfile, user=other)
    if myprofile != otherprofile:
        myprofile.following.add(otherprofile)
        myprofile.save()
        #adding to uncategorized, gotta check if exists or not
        if Category.objects.filter(name='Uncategorized', owner=myprofile).count() == 0:
            cat = Category.objects.create(name='Uncategorized', owner=myprofile)
        else:
            cat = Category.objects.get(name='Uncategorized', owner=myprofile)
        #note: this will uncategorize otheruser if they're already followed and already categorized. This is a "bug" but to fix it I would have to search all categories to see if otheruser exists there or not
        addToCategory(myprofile, otherprofile, cat)
    
    followlist = myprofile.following.all()
    all_categories = Category.objects.filter(owner=myprofile)

    return HttpResponseRedirect('/following/')

#request is the user who is requesting the operation to happen
#category is which category that the user which to place the otheruser into
@login_required(login_url='/login/')
def categorize(request, otheruser, category):
    if request.user.is_authenticated():
        user = request.user.username

    #categorizing portion
    myself = get_object_or_404(User, username=request.user.username)
    myprofile = get_object_or_404(UserProfile, user=myself)

    other = get_object_or_404(User, username=otheruser)
    otherprofile = get_object_or_404(UserProfile, user=other)

    #check if otherprofile is actually being followed or not
    if otherprofile in myprofile.following.all():
        cat = Category.objects.get(owner=myprofile, name=category)
        addToCategory(myprofile, otherprofile, cat)
    followlist = myprofile.following.all()
    all_categories = Category.objects.filter(owner=myprofile)

    return HttpResponseRedirect('/following/')

@login_required(login_url='/login/')
def view_category(request, category):
    if request.user.is_authenticated():
        user = request.user.username

    #categorizing portion
    myself = get_object_or_404(User, username=request.user.username)
    myprofile = get_object_or_404(UserProfile, user=myself)

    single_category = Category.objects.filter(name=category, owner=myprofile)
    
    #[0] is because there should only be 1
    users_in_category = single_category[0].categorized_users.all()

    return render_to_response('following/category.html', 
                              {'users_in_category':users_in_category,
                              'number_of_users_in_category':users_in_category.count(),
                              'category_name':category},
                              context_instance=RequestContext(request))

@login_required(login_url='/login/')
def delete_category(request, category):
    if request.user.is_authenticated():
        user = request.user.username
    myself = get_object_or_404(User, username=request.user.username)
    myprofile = get_object_or_404(UserProfile, user=myself)
    followlist = myprofile.following.all()

    # cannot delete Uncategorized
    if not category == 'Uncategorized':
        uncategorized = Category.objects.get(owner=myprofile, name='Uncategorized')
        to_delete = Category.objects.get(owner=myprofile, name=category)
        list_of_relations = to_delete.categorized_users.all()
        for otheruser in list_of_relations:
            uncategorized.categorized_users.add(otheruser)
            to_delete.categorized_users.remove(otheruser)
        to_delete.delete()
        
    all_categories = Category.objects.filter(owner=myprofile)
    return HttpResponseRedirect('/following/')
