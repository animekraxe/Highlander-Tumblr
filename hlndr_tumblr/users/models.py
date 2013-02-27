from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from blog.models import Like

# Create your models here.
class UserProfile(models.Model):
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
		if post.author != self.user:
			exec "Like.objects.get_or_create(%s=post, user=self.user)" % (post.classname().lower())

	def send_friend_request(self, receiver):
		FriendRequest.objects.get_or_create(sender=self.user, receiver=receiver)
