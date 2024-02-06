from django import forms

class ConstructorOptionsForm(forms.Form):
	OPTIONS = [
		('option1', 'Type Tesla'),
		('option2', 'Type 1'),
		('option3', 'Type 2'),
	]

	name = forms.ChoiceField(choices=OPTIONS, widget=forms.Select(attrs={'class': 'your-css-class'}))