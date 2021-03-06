from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from blog.models import *

# Create your models here.

class FaveList(models.Model):
	user = models.OneToOneField(User)
	textlist = models.ManyToManyField(TextPost, related_name="list_text")
	photolist = models.ManyToManyField(PhotoPost, related_name="list_photo")
	videolist = models.ManyToManyField(VideoPost, related_name="list_video")
	audiolist = models.ManyToManyField(AudioPost, related_name="list_audio")
	quotelist = models.ManyToManyField(QuotePost, related_name="list_quote")
	linklist = models.ManyToManyField(LinkPost, related_name="list_link")
	chatlist = models.ManyToManyField(ChatPost, related_name="list_chat")

	def __unicode__(self):
		return self.user.username

	def get_favorites(self):
		textlist = list(self.textlist.all())
		photolist = list(self.photolist.all())
		videolist = list(self.videolist.all())
		audiolist = list(self.audiolist.all())
		quotelist = list(self.quotelist.all())
		linklist = list(self.linklist.all())
		chatlist = list(self.chatlist.all())
		return textlist + photolist + videolist + audiolist + quotelist + linklist + chatlist

	def add(self, post):
		post_type = post.classname()
		post_id = post.id
		if post_type == 'TextPost':
			post = get_object_or_404(TextPost, id=post_id)
			self.textlist.add(post)
		elif post_type == 'PhotoPost':
			post = get_object_or_404(PhotoPost, id=post_id)
			self.photolist.add(post)
		elif post_type == 'VideoPost':
			post = get_object_or_404(VideoPost, id=post_id)
			self.videolist.add(post)
		elif post_type == 'AudioPost':
			post = get_object_or_404(AudioPost, id=post_id)
			self.audiolist.add(post)
		elif post_type == 'QuotePost':
			post = get_object_or_404(QuotePost, id=post_id)
			self.quotelist.add(post)
		elif post_type == 'LinkPost':
			post = get_object_or_404(LinkPost, id=post_id)
			self.linklist.add(post)
		elif post_type == 'ChatPost':
			post = get_object_or_404(ChatPost, id=post_id)
			self.chatlist.add(post)
		return None

	def delete(self, post):
		post_type = post.classname()
		post_id = post.id
		if post_type == 'TextPost':
			post = get_object_or_404(TextPost, id=post_id)
			self.textlist.remove(post)
		elif post_type == 'PhotoPost':
			post = get_object_or_404(PhotoPost, id=post_id)
			self.photolist.remove(post)
		elif post_type == 'VideoPost':
			post = get_object_or_404(VideoPost, id=post_id)
			self.videolist.remove(post)
		elif post_type == 'AudioPost':
			post = get_object_or_404(AudioPost, id=post_id)
			self.audiolist.remove(post)
		elif post_type == 'QuotePost':
			post = get_object_or_404(QuotePost, id=post_id)
			self.quotelist.remove(post)
		elif post_type == 'LinkPost':
			post = get_object_or_404(LinkPost, id=post_id)
			self.linklist.remove(post)
		elif post_type == 'ChatPost':
			post = get_object_or_404(ChatPost, id=post_id)
			self.chatlist.remove(post)
		return None
