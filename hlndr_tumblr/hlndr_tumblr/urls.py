from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hlndr_tumblr.views.home', name='home'),
    # url(r'^hlndr_tumblr/', include('hlndr_tumblr.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

	# home page 
	url(r'^$', 'hlndr_tumblr.views.home', name='home'),
	url(r'^register/$', 'users.views.register', name='register'),
	url(r'^login/$', 'users.views.log_in', name='log_in'),
	url(r'^logout/$', 'users.views.log_out', name='log_out'),
	url(r'^dashboard/$', 'dashboard.views.dashboard', name='dashboard'),

	url(r'^post/(?P<post_type>\w+)/(?P<post_id>\d+)/$', 'blog.views.post_page', name='post_page'),
	url(r'^new/', include('blog.urls')),

	url(r'^messages/', include('messages.urls')),

	url(r'^delete/(?P<post_type>\w+)/(?P<post_id>\d+)/$', 'dashboard.views.deletepost', name='deletepost'),

	url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.ico'}),

   	url(r'^following/$', 'following.views.following', name='following'),
  	url(r'^follow/(?P<username>\w+)/$', 'following.views.follow', name='follow'),
 	url(r'^following/delete/(?P<category>[\w@.+\-\ ]+)/$','following.views.delete_category', name='delete_category'),
	url(r'^following/category/(?P<category>[\w@.+\-\ ]+)/$', 'following.views.view_category', name = 'view_category'),
	url(r'^following/categorize/(?P<category>[\w@.+\-\ ]+)/(?P<otheruser>\w+)/$', 'following.views.categorize', name='categorize'),

	url(r'^editprofile/$', 'users.views.edit_profile', name="edit_profile"),

	url(r'^postaction/(?P<username>\w+)/$', 'blog.views.blog_post_action', name='blog_post_action'),

	url(r'^(?P<username>\w+)/$', 'blog.views.blogpage', name='blogpage'),
	url(r'^(?P<username>\w+)/posts/$', 'dashboard.views.viewposts', name='viewposts'),
	url(r'^(?P<username>\w+)/profile/$', 'users.views.profile', name='profile'),
	#Friends page, yet to have an actual html page
	#url(r'^(?P<username>\w+)/friends/$', 'friend_page', name='friend_page'),
)
