from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^comment/(?P<post_type>\w+)/(?P<post_id>\d+)/$', 'blog.views.new_comment', name='newcomment'),
	url(r'^text/$', 'blog.views.new_text_post', name='newtext'),
	url(r'^photo/$', 'blog.views.new_photo_post', name='newphoto'),
	url(r'^quote/$', 'blog.views.new_quote_post', name='newquote'),
	url(r'^link/$', 'blog.views.new_link_post', name='newlink'),
	url(r'^chat/$', 'blog.views.new_chat_post', name='newchat'),
	url(r'^audio/$', 'blog.views.new_audio_post', name='newaudio'), 
	url(r'^video/$', 'blog.views.new_video_post', name='newvideo'),
)	
