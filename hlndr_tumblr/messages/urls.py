from django.conf.urls import patterns, include, url

urlpatterns = patterns('messages.views',
	url(r'^$', 'inbox', name='messages'),
	url(r'^inbox/$', 'inbox', name='messages_inbox'),
	url(r'^compose/$', 'compose', name='messages_compose'),
)
