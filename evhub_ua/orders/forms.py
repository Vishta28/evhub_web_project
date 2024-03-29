from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ('first_name', 'last_name', 'phone_number')

		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'form-control rounded-0', 'placeholder': "Ваше ім'я"}),
			'last_name': forms.TextInput(attrs={'class': 'form-control rounded-0', 'placeholder': "Ваше призвіще"}),
			'phone_number': forms.TextInput(attrs={'class': 'form-control rounded-0', 'placeholder': "Номер телефону"}),
		}
