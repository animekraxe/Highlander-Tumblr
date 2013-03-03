from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist

from taggit.managers import TaggableManager
from constants import *

# Create your models here.

# Encapsulates blog specific information
class Blog(models.Model):
	author = models.ForeignKey(User)
	title = models.CharField(max_length=100, default="Untitled")

class TextPost(models.Model):
	title = models.CharField(max_length=100)
	slug = models.SlugField()
	text = models.TextField()
	post_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User)
	privacy = models.IntegerField(choices=privacy_choices, default=PRIVACY_ALL)
	tags = TaggableManager()

	def __unicode__(self):
		return "author:%s, title:%s, post_date:%s" % (self.author.username, 
													  self.title, 
													  self.post_date)

	def classname(self):
		return self.__class__.__name__

	def custom_html(self):
		html = "<h3>" + self.title + "</h3>"
		html += "<h6>" + self.text + "</h6>"
		return html

class PhotoPost(models.Model):
	filename = models.CharField(max_length=100)
	url = models.URLField()
	caption = models.TextField()
	post_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User)
	privacy = models.IntegerField(choices=privacy_choices, default=PRIVACY_ALL)
	tags = TaggableManager()

	def __unicode__(self):
		return "author:%s, filename:%s, post_date:%s" % (self.author.username,
													     self.filename,
														 self.post_date)

	def classname(self):
		return self.__class__.__name__

	def custom_html(self):
		html = """ <img src=" """ + self.url + """ "></img> """
		html += "<h6>" + self.caption + "</h6>"
		return html
	
class VideoPost(models.Model):
	filename = models.CharField(max_length=100)
	url = models.URLField()
	description = models.TextField()
	post_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User)
	privacy = models.IntegerField(choices=privacy_choices, default=PRIVACY_ALL)

	tags = TaggableManager()

	def __unicode__(self):
		return "author:%s, filename:%s, post_date:%s" % (self.author.username,
													     self.filename,
														 self.post_date)

	def classname(self):
		return self.__class__.__name__

	def custom_html(self):
		html = """ <video width="100%" controls> """
		html += """ <source src="%s" type="vidoe/mp4"> """ % self.url
		html += """ <p> Could not play </p> """
		html += """ </video> """
		html += """ <h6> %s </h6> """ % self.description
		return html

class AudioPost(models.Model):
	filename = models.CharField(max_length=100)
	url = models.URLField()
	description = models.TextField()
	post_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User)
	privacy = models.IntegerField(choices=privacy_choices, default=PRIVACY_ALL)

	tags = TaggableManager()

	def __unicode__(self):
		return "author:%s, filename:%s, post_date:%s" % (self.author.username,
													     self.filename,
														 self.post_date)

	def classname(self):
		return self.__class__.__name__

	def custom_html(self):
		html = """ <audio controls> """
		html += """ <source src="%s" type="audio/mpeg"> """ % self.url
		html += """ <p> Could not play </p> """
		html += """ </audio> """
		html += """ <h6> %s </h6> """ % self.description
		return html

class QuotePost(models.Model):
	quote = models.TextField()
	source = models.TextField()
	post_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User)
	privacy = models.IntegerField(choices=privacy_choices, default=PRIVACY_ALL)

	tags = TaggableManager()

	def __unicode__(self):
		return "author:%s, post_date:%s" % (self.author.username, self.post_date)
	
	def classname(self):
		return self.__class__.__name__

	def custom_html(self):
		html = """ <h1> "%s" </h1> """ % self.quote
		html += """ <h5> -%s </h5> """ % self.source
		return html

class LinkPost(models.Model):
	title = models.CharField(max_length=100)
	link = models.URLField()
	description = models.TextField()
	post_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User)
	privacy = models.IntegerField(choices=privacy_choices, default=PRIVACY_ALL)

	tags = TaggableManager()

	def __unicode__(self):
		return "author:%s, title:%s, post_date:%s" % (self.author.username,
													  self.title,
													  self.post_date)
	def classname(self):
		return self.__class__.__name__

	def custom_html(self):
		html = """ <div class="well container-fluid" style="background-color:#F5F6CE;"> """
		html += """ <a href="%s" class="btn btn-link"><strong> %s </strong></a> """ % (self.link, self.link)
		html += """ </div> """
		html += """ <h2> %s </h2> """ % self.title
		html += """ <h6> %s </h6> """ % self.description
		return html

class ChatPost(models.Model):
	title = models.CharField(max_length=100)
	chat = models.TextField()
	post_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User)
	privacy = models.IntegerField(choices=privacy_choices, default=PRIVACY_ALL)

	tags = TaggableManager()

	def __unicode__(self):
		return "author:%s, title:%s, post_date:%s" % (self.author.username,
												      self.title,
													  self.post_date)
	def classname(self):
		return self.__class__.__name__

	def custom_html(self):
		html = """ <h3> %s </h3> """ % self.title
		html += """ <h5> %s </h5> """ % self.chat
		return html

# todo: implement comments and likes and reposts
class Like(models.Model):
	textpost = models.ForeignKey(TextPost, null=True)
	photopost = models.ForeignKey(PhotoPost, null=True)
	quotepost = models.ForeignKey(QuotePost, null=True)
	linkpost = models.ForeignKey(LinkPost, null=True)
	chatpost = models.ForeignKey(ChatPost, null=True)
	audiopost = models.ForeignKey(AudioPost, null=True)
	videopost = models.ForeignKey(VideoPost, null=True)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.user.username + ',' + self.get_post().classname()

	def get_post(self):
		if self.textpost != None:
			return self.textpost
		if self.photopost != None:
			return self.photopost
		if self.quotepost != None:
			return self.quotepost
		if self.linkpost != None:
			return self.linkpost
		if self.chatpost != None:
			return self.chatpost
		if self.audiopost != None:
			return self.audiopost
		if self.videopost != None:
			return self.videopost

		return None

class Comment(models.Model):
	textpost = models.ForeignKey(TextPost, null=True)
	photopost = models.ForeignKey(PhotoPost, null=True)
	quotepost = models.ForeignKey(QuotePost, null=True)
	linkpost = models.ForeignKey(LinkPost, null=True)
	chatpost = models.ForeignKey(ChatPost, null=True)
	audiopost = models.ForeignKey(AudioPost, null=True)
	videopost = models.ForeignKey(VideoPost, null=True)

	user = models.ForeignKey(User)
	comment = models.TextField()
	post_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.user.username + ',' + self.get_post().classname()

	def get_post(self):
		if self.textpost != None:
			return self.textpost
		if self.photopost != None:
			return self.photopost
		if self.quotepost != None:
			return self.quotepost
		if self.linkpost != None:
			return self.linkpost
		if self.chatpost != None:
			return self.chatpost
		if self.audiopost != None:
			return self.audiopost
		if self.videopost != None:
			return self.videopost

		return None

