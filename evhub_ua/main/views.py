from django.views.generic import View
from django.shortcuts import redirect, render

class ActiveButtonsView(View):
	template_name = 'main/active_buttons.html'

	def get(self, request):
		context = self.request.GET.get('q')
		print(context)
		return render(request, self.template_name, {'context': context})