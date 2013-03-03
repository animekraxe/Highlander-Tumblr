from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notification(models.Model):
	user = models.ForeignKey(User)
	message = models.CharField(max_length=200)
	link = models.CharField(max_length=200)	
