from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from blog.models import Like

# friend request relation
class FriendRequest(models.Model):
	sender = models.ForeignKey(User, related_name='friendrequest_sender')
	receiver = models.ForeignKey(User, related_name='friendrequest_receiver')

	def __unicode__(self):
		return self.sender.username + ',' + self.receiver.username

# Create your models here.
class UserProfile(models.Model):
  	GENDER_CHOICES = (
		('u', 'Undisclosed'),
		('m', 'Male'),
		('f', 'Female'),
	)
    
	user = models.OneToOneField(User)
    
    #following logic
	following = models.ManyToManyField('UserProfile', related_name="list_following")

	#friends list
	friends = models.ManyToManyField('UserProfile', related_name="list_friends")
    
	# URL to avatar image hosted
	avatar = models.URLField()
	nickname = models.CharField(max_length=50, blank=True)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
	birthday = models.DateField()
	interests = models.CharField(max_length=500, blank=True)

	def __unicode__(self):
        #prepended with 'self.' to resolve scoping issues within the shell
		return self.user.username

	# like a particular post
	def like_post(self, post):
		classname = post.classname()
		if classname == "TextPost":
			Like.objects.get_or_create(textpost=post, user=self.user)
		elif classname == "PhotoPost":
			Like.objects.get_or_create(photopost=post, user=self.user)
		elif classname == "LinkPost":
			Like.objects.get_or_create(linkpost=post, user=self.user)
		elif classname == "QuotePost":
			Like.objects.get_or_create(quotepost=post, user=self.user)
		elif classname == "ChatPost":
			Like.objects.get_or_create(chatpost=post, user=self.user)
		elif classname == "AudioPost":
			Like.objects.get_or_create(audiopost=post, user=self.user)
		elif classname == "VideoPost":
			Like.objects.get_or_create(videopost=post, user=self.user)
		
		return None

	def send_friend_request(self, receiver):
		FriendRequest.objects.get_or_create(sender=self.user, receiver=receiver)
