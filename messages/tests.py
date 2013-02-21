"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.contrib.auth.models import User
from messages.models import Message
from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

	def test_empty_message_list(self):
		recipient = User.objects.get(username="test")
		message_list = Message.objects.filter(recipient=recipient)
		
		self.assertEqual(message_list, None)	
