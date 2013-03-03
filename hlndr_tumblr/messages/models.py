from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
	sender = models.ForeignKey(User, related_name='message_sender')
	recipient = models.ForeignKey(User, related_name='message_recipient')
	title = models.CharField(max_length=200)
	message = models.TextField()
	send_date = models.DateTimeField(auto_now_add=True)
	is_new = models.BooleanField(default=True)
	
	def __unicode__(self):
		return self.sender.username + ',' + self.recipient.username + ', title:' + self.title
	
