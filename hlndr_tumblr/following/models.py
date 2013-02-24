from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile

# Create your models here.
#class Categories(models.Model):
	

class Category(models.Model):
	def __unicode__(self):
		return self.name
	name = models.CharField(max_length=30)
#remember to take out the null/blank as a category object w/o an owner is nonsense
	owner = models.ForeignKey(UserProfile, related_name="the_owner")
	categorized_users = models.ManyToManyField(UserProfile, null=True, blank=True, related_name="users_belonging_to_this_category")

