from django.views.generic import View
from django.shortcuts import redirect, render
from django_user_agents.utils import get_user_agent

# стартова сторінка
def welcome_page(request):
	user_agent = get_user_agent(request)
	if user_agent.is_mobile:
		return render(request, 'main/welcome_mob.html')
	else:
		return render(request, 'main/welcome.html')

def contact_info(request):
	return render(request, 'main/contact_info.html')

class ActiveButtonsView(View):
	template_name = 'main/active_buttons.html'

	def get(self, request):
		context = self.request.GET.get('q')
		print(context)
		return render(request, self.template_name, {'context': context})