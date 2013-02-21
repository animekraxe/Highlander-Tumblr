from django import forms

class ComposeMessageForm(forms.Form):
	recipient = forms.CharField(max_length=30)
	title = forms.CharField(max_length=200, required=False)
	message = forms.CharField()
