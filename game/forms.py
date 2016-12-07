from django import forms
from .models import Input

class inputForm(forms.ModelForm, input):
	chosen_answer = forms.ChoiceField(choices = input.answers )
	class Meta:
		model = Input
		fields = []

