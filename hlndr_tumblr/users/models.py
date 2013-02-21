from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

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

	def send_friend_request(self, receiver):
		FriendRequest.objects.get_or_create(sender=self.user, receiver=receiver)
