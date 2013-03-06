from django import forms
from blog.constants import *

class CommentForm(forms.Form):
	comment = forms.CharField(required=True)

class ReblogForm(forms.Form):
	description = forms.CharField(required=True)

class TextForm(forms.Form):
	title = forms.CharField(max_length=100, required=False)
	text = forms.CharField(required=True)
	tags = forms.CharField(required=False)
	privacy = forms.ChoiceField(widget=forms.Select(attrs={'class':'span3'}),
								choices=privacy_choices,
								required=True)

class PhotoForm(forms.Form):
	photo = forms.FileField(required=True)
	caption = forms.CharField(required=False)
	tags = forms.CharField(required=False)
	privacy = forms.ChoiceField(widget=forms.Select(attrs={'class':'span3'}),
								choices=privacy_choices,
								required=True)

class VideoForm(forms.Form):
	video = forms.FileField(required=True)
	description = forms.CharField(required=False)
	tags = forms.CharField(required=False)
	privacy = forms.ChoiceField(widget=forms.Select(attrs={'class':'span3'}),
								choices=privacy_choices,
								required=True)

class AudioForm(forms.Form):
	audio = forms.FileField(required=True)
	description = forms.CharField(required=False)
	tags = forms.CharField(required=False)
	privacy = forms.ChoiceField(widget=forms.Select(attrs={'class':'span3'}),
								choices=privacy_choices,
								required=True)

class QuoteForm(forms.Form):
	quote = forms.CharField(required=True)
	source = forms.CharField(required=False)
	tags = forms.CharField(required=False)
	privacy = forms.ChoiceField(widget=forms.Select(attrs={'class':'span3'}),
								choices=privacy_choices,
								required=True)

class LinkForm(forms.Form):
	title = forms.CharField(max_length=100, required=False)
	link = forms.URLField(required=True)
	description = forms.CharField(required=False)
	tags = forms.CharField(required=False)
	privacy = forms.ChoiceField(widget=forms.Select(attrs={'class':'span3'}),
								choices=privacy_choices,
								required=True)

class ChatForm(forms.Form):
	title = forms.CharField(max_length=100, required=False)
	chat = forms.CharField(required=True)
	tags = forms.CharField(required=False)
	privacy = forms.ChoiceField(widget=forms.Select(attrs={'class':'span3'}),
								choices=privacy_choices,
								required=True)

