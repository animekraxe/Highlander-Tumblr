from django import forms

class CreateCategoryForm(forms.Form):
    #new_category = forms.CharField()
    new_category = forms.RegexField(regex=r'^[\ \w.@+-]+$',
                                    max_length=20,
                                    label="new_category",
                                    error_messages={'invalid':"You may only use letters and numbers"})
